#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys
from typing import List

logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------------- #
#                                    Common                                    #
# ---------------------------------------------------------------------------- #
def run(cmd: str, capture_output=True) -> str:
    if capture_output == False:
        logging.info(f"Running command:{cmd}")
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
def get_build_arguments(distribution: str, sources: str) -> str:

    build_args = ""

    # ---------------------------------- UserID ---------------------------------- #
    build_args += f'--build-arg UID="{get_uid()}"'

    # ---------------------------------- Sources --------------------------------- #
    try:
        with open(f"/etc/dpkg-buildenv/sources.list.d/{sources}.sources") as file:
            additional_sources = file.read().replace("\n", "\\n")
            build_args += f' --build-arg ADDITIONAL_SOURCES="{additional_sources}"'
    except FileNotFoundError:
        if sources != "default":
            sys.exit(
                f"Error file not found: /etc/dpkg-buildenv/sources.list.d/{sources}.sources"
            )

    # ------------------------------- Distribution ------------------------------- #
    if distribution:
        build_args += f" --build-arg DISTRIBUTION={distribution}"

    return build_args


def build_image(repository_name: str, no_cache: str = "", build_arguments: str = ""):
    build_cmd = f"""\
podman image build
--tag {repository_name}
--file /home/aidan/Code/Per/dpkg-buildenv/dpkg-buildenv/Dockerfile
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
def run_container(repository_name: str, command: str = "", interactive: str = ""):
    # ------------------------ Handle docker run arguments ----------------------- #
    # If the user hasn't supplied a command then assume build command.
    # Delete built_packages to clear out any old packages then move new ones over.

#podman unshare chown 1000:1000 -R .

# TODO: How can I do this without sudo?
    if command == "":
        command = f"""\
sudo dpkg-buildpackage && \
sudo mv-debs && \
sudo dpkg-buildpackage --target=clean\
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
podman run
--mount type=bind,src=${{PWD}},dst=/workspaces/code
--user {get_uid()}:$(id -g {get_uid()})
--network host
--tty
--rm
--env DEB_BUILD_OPTIONS={deb_build_options}
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
    run(f"mv built_packages/*.deb {destination}")
    run("rm -r built_packages/")


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
def dpkg_buildenv_parse_args(argv: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nc",
        "--no-cache",
        help="Do not use cache when building the image.",
        action="store_const",
        default="",
        const="--no-cache",
    )
    parser.add_argument(
        "-s",
        "--sources",
        help="Select a sources file stored at /etc/dpkg-buildenv/sources.list.d/<SOURCE>.list.",
        default="default",
    )
    parser.add_argument(
        "-d",
        "--distribution",
        help="Select a linux distribution for the docker parent image (e.g.debian:11).",
        default=None,
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
        help="Delete all build environment images generated by this tool",
        action="store_true",
    )
    args = parser.parse_args(argv)

    return args


def main(argv: List[str]):
    try:
        args = dpkg_buildenv_parse_args(argv)

        if args.delete_images:
            delete_images()
            sys.exit()

        build_arguments = get_build_arguments(args.distribution, args.sources)
        if args.get_build_arguments:
            print(build_arguments)
            sys.exit()

        prerequisite_check()
        repository_name = generate_image_name()
        build_image(repository_name, args.no_cache, build_arguments)
        run_container(repository_name, args.command, args.interactive)

        if args.destination:
            move_built_packages(args.destination)

    except KeyboardInterrupt:
        kill_container(repository_name)
        sys.exit(130)


if __name__ == "__main__":
    main(sys.argv[1:])

# ---------------------------------------------------------------------------- #
