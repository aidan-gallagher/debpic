#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys
import yaml
from typing import List
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="%(message)s")

# ---------------------------------------------------------------------------- #
#                                    Common                                    #
# ---------------------------------------------------------------------------- #
def run(cmd: str, capture_output=True) -> str:
    if capture_output == False:
        green_txt_start = "\033[92m"
        bold_txt_start = "\033[1m"
        fmt_txt_end = "\033[0m"
        logging.info(
            f"{bold_txt_start}{green_txt_start}Running command:{fmt_txt_end} {green_txt_start}{cmd}{fmt_txt_end}"
        )
    return subprocess.run(
        cmd, shell=True, text=True, capture_output=capture_output, check=True
    ).stdout


def prerequisite_check():

    # Check the user can run docker without sudo
    result = subprocess.run(
        "docker info", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if result.returncode != 0:
        sys.exit(
            """\
You must allow docker to run as non-root user
To do this follow the steps in the official docker documentation: https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
Run the following:
sudo usermod -aG docker $USER
newgrp docker"""
        )

    # Check correct directory
    if not os.path.isfile("./debian/control"):
        sys.exit(
            f"Could not find /debian/control file. Are you in the correct directory?"
        )

    # Check ccache directory exists
    run("mkdir -p $HOME/.cache/ccache")


def delete_images():
    find_result = run("docker images '*buildenv' --format {{.Repository}}").replace(
        "\n", " "
    )

    if find_result != "":
        run(f"docker rmi {find_result}; docker image prune --force")
    else:
        logging.info("No images to delete")


def generate_image_name() -> str:
    path = os.getcwd()
    directories = os.path.split(path)
    image_name = directories[-1].lower() + "-buildenv"
    return image_name


def get_uid() -> int:
    uid = os.getuid()
    if uid == 0:
        uid = int(os.environ.get("SUDO_UID", "1000"))
    return uid


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                     Build                                    #
# ---------------------------------------------------------------------------- #
@contextmanager
def hardlink_local_repository(local_repository_path: str):
    # Docker can't access files outwith it's build context.
    # This adds the contents of the local_repository into the build context.
    if local_repository_path:
        if not os.path.isdir(local_repository_path):
            sys.exit(f'Local repository "{local_repository_path}" is not a directory')
        run("rm -rf ./local_repository && mkdir --parents ./local_repository")
        run(f"ln {local_repository_path}/* ./local_repository/")

    yield

    if local_repository_path:
        run("rm -rf ./local_repository")


def get_build_arguments(distribution: str, sources: str, extra_pkgs: List) -> str:

    build_args = ""

    # ------------------------------- Distribution ------------------------------- #
    if distribution:
        build_args += f" --build-arg DISTRIBUTION={distribution}"

    # ---------------------------------- UserID ---------------------------------- #
    build_args += f' --build-arg UID="{get_uid()}"'

    # -------------------------------- Extra pkgs -------------------------------- #
    if len(extra_pkgs) > 0:
        build_args += f" --build-arg EXTRA_PKGS=\"{' '.join(extra_pkgs)}\""

    # ---------------------------------- Sources --------------------------------- #
    try:
        with open(f"/etc/debpic/sources.list.d/{sources}.sources") as file:
            additional_sources = file.read().replace("\n", "\\n")
            build_args += f' --build-arg ADDITIONAL_SOURCES="{additional_sources}"'
    except FileNotFoundError:
        if sources != "default":
            sys.exit(
                f"Error file not found: /etc/debpic/sources.list.d/{sources}.sources"
            )

    return build_args


def build_image(repository_name: str, no_cache: str = "", build_arguments: str = ""):
    build_cmd = f"""\
DOCKER_BUILDKIT=1
docker image build
--tag {repository_name}
--file /usr/share/debpic/Dockerfile
--network host
{no_cache}
{build_arguments}
.\
""".replace(
        "\n", " "
    )

    run(build_cmd, capture_output=False)


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                      Run                                     #
# ---------------------------------------------------------------------------- #
def run_container(
    repository_name: str,
    command: str = "",
    dpkg_buildpackage_args: str = "",
    interactive: str = "",
):
    # ------------------------ Handle docker run arguments ----------------------- #
    # If the user hasn't supplied a command then assume build command.
    # Delete built_packages to clear out any old packages then move new ones over.
    if command == "":
        command = f"""\
dpkg-buildpackage {dpkg_buildpackage_args} && \
mv-debs && \
dpkg-buildpackage --target=clean\
""".replace(
            "\n", " "
        )

    # Regardless of command origin (user provided or assumed), prepend the
    # command with "/bin/bash -c".
    command = f"/bin/bash -c '{command}'"

    # If interactive mode is specified then remove any commands
    if interactive != "":
        command = ""

    deb_build_options = os.environ.get("DEB_BUILD_OPTIONS", "")

    run_cmd = f"""\
docker run
--mount type=bind,src=${{PWD}},dst=/workspaces/code
--mount type=bind,src=${{HOME}}/.cache/ccache,dst=/home/docker/.cache/ccache
--user {get_uid()}:$(id -g {get_uid()})
--network host
--tty
--rm
--env DEB_BUILD_OPTIONS="{deb_build_options}"
{interactive}
{repository_name}
{command}\
""".replace(
        "\n", " "
    )

    try:
        result = run(run_cmd, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"Build failed!")
        sys.exit(e.returncode)


def move_built_packages(destination):
    run(f"mkdir --parents {destination}")
    run(f"[ ! -d built_packages ] || mv built_packages/*.deb {destination}")
    run("rm -rf built_packages/")


def kill_container(repository_name):
    result = run(
        f"docker ps --all --quiet --filter ancestor={repository_name}"
    ).replace("\n", " ")
    if result != "":
        run(f"docker kill {result}")


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
def debpic_parse_args(argv: List[str]):

    # Customer formatter required to print help message for "--" option.
    class CustomHelpFormatter(argparse.HelpFormatter):
        def format_help(self):
            original_help = super().format_help()
            return (
                original_help + "  --\t\t\tArguments to pass to dpkg-buildpackage. \n"
            )

    def read_config(filename: str, config: dict):
        # Read defaults from configuration file.
        # Save config read_config.prev_config.
        # combined_config = prev_config + new config from file (preferred)
        try:
            with open(filename, "r") as f:
                try:
                    new_config = yaml.safe_load(f)
                    if new_config:
                        combined_config = {**config, **new_config}
                        return combined_config
                except yaml.parser.ParserError:
                    sys.exit(f"Bad format in config file: {filename}")
        except FileNotFoundError:
            pass

        return config

    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    parser.add_argument(
        "-nc",
        "--no-cache",
        help="Do not use cache when building the image.",
        action="store_const",
        default="",
        const="--no-cache",
    )
    parser.add_argument(
        "-d",
        "--distribution",
        help="Select a linux distribution for the docker parent image (e.g.debian:11).",
        default=None,
    )
    parser.add_argument(
        "-lr",
        "--local-repository",
        help="Local path to folder with .debs to be used as local apt repository. Defaults to ./local_repository.",
        # Default handled in dockerfile
    )
    parser.add_argument(
        "-s",
        "--sources",
        help="Select a sources file stored at /etc/debpic/sources.list.d/<SOURCE>.list.",
        default="default",
    )
    parser.add_argument(
        "-ep",
        "--extra-pkg",
        help="Extra package to install in the container. This option can be specified multiple times for multiple packages.",
        action="append",
        default=[],
    )
    parser.add_argument(
        "-dst",
        "--destination",
        help="Chose a destination directory to store built debian packages.",
        default=None,
    )
    parser.add_argument(
        "--get-build-arguments",
        # Help suppressed as this option is generally only used by tools such as Jenkins
        help=argparse.SUPPRESS,
        action="store_true",
    )
    exclusive_group_parser = parser.add_mutually_exclusive_group()
    exclusive_group_parser.add_argument(
        "-i",
        "--interactive",
        help="Open an interactive terminal to the container.",
        action="store_const",
        default="",
        const="--interactive",
    )
    exclusive_group_parser.add_argument(
        "command",
        help="Command to execute in the container.",
        nargs="?",
        default="",
    )
    exclusive_group_parser.add_argument(
        "-di",
        "--delete-images",
        help="Delete all build environment images generated by this tool.",
        action="store_true",
    )

    SYSTEM_CONFIG_FILE = os.path.expanduser("/etc/debpic/debpic.conf")
    USER_CONFIG_FILE = os.path.expanduser("~/.config/debpic/debpic.conf")
    REPO_CONFIG_FILE = os.path.expanduser("./debpic.conf")
    system_config = read_config(SYSTEM_CONFIG_FILE, {})
    user_config = read_config(USER_CONFIG_FILE, system_config)
    repo_config = read_config(REPO_CONFIG_FILE, user_config)
    parser.set_defaults(**repo_config)

    # Extract dpkg-buildpackage ("--") args before argparse parsing
    for idx, arg in enumerate(argv):
        if arg == "--":
            debpic_args = argv[:idx]
            dpkg_buildpackage_args = argv[idx + 1 :]
            break
    else:
        debpic_args = argv
        dpkg_buildpackage_args = [""]

    args = parser.parse_args(debpic_args)
    args.dpkg_buildpackage_args = " ".join(dpkg_buildpackage_args)

    return args


def main(argv: List[str]):
    try:
        args = debpic_parse_args(argv)

        if args.delete_images:
            delete_images()
            sys.exit()

        build_arguments = get_build_arguments(
            args.distribution, args.sources, args.extra_pkg
        )
        if args.get_build_arguments:
            print(build_arguments)
            sys.exit()

        prerequisite_check()
        repository_name = generate_image_name()
        with hardlink_local_repository(args.local_repository):
            build_image(repository_name, args.no_cache, build_arguments)
        run_container(
            repository_name, args.command, args.dpkg_buildpackage_args, args.interactive
        )

        if args.destination:
            move_built_packages(args.destination)

    except KeyboardInterrupt:
        kill_container(repository_name)
        sys.exit(130)


if __name__ == "__main__":
    main(sys.argv[1:])

# ---------------------------------------------------------------------------- #
