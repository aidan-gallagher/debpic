import os
import sys
from contextlib import contextmanager
from typing import List

import common


@contextmanager
def hardlink_local_repository(local_repository_path: str):
    # Docker can't access files outwith it's build context.
    # This adds the contents of the local_repository into the build context.
    if local_repository_path:
        if not os.path.isdir(local_repository_path):
            sys.exit(f'Local repository "{local_repository_path}" is not a directory')
        common.run("rm -rf ./local_repository && mkdir --parents ./local_repository")
        common.run(f"ln {local_repository_path}/*.deb ./local_repository/")

    yield

    if local_repository_path:
        common.run("rm -rf ./local_repository")


@contextmanager
def copy_hook(hook_filename: str):
    hook_path = f"/etc/debpic/hooks/{hook_filename}"

    # Check hook file exists and is valid
    if not os.path.isfile(hook_path):
        if hook_filename != "default":
            sys.exit(f"{hook_path} does not exist")
    else:
        if not os.access(hook_path, os.X_OK):
            common.run(f"chmod +x {hook_path}")

        common.run(f"cp {hook_path} ./debpic_hook")

    yield

    if os.path.isfile("./debpic_hook"):
        common.run(f"rm ./debpic_hook")


def read_sources_and_preferences_files(sources: str):
    filename = f"/etc/debpic/sources.list.d/{sources}.sources"
    try:
        with open(filename) as file:
            additional_sources = file.read().replace("\n", "\\n")
    except FileNotFoundError:
        if sources != "default":
            sys.exit(f"Error file not found: {filename}")
        additional_sources = ""

    filename = f"/etc/debpic/preferences.d/{sources}.pref"
    try:
        with open(filename) as file:
            additional_preferences = file.read().replace("\n", "\\n")
    except FileNotFoundError:
        additional_preferences = ""

    return additional_sources, additional_preferences


def get_build_arguments(distribution: str, sources: str, extra_pkgs: List) -> str:
    build_args = ""

    # ------------------------------- Distribution ------------------------------- #
    if distribution:
        build_args += f" --build-arg DISTRIBUTION={distribution}"

    # ---------------------------------- UserID ---------------------------------- #
    build_args += f' --build-arg UID="{common.get_uid()}"'

    # -------------------------------- Extra pkgs -------------------------------- #
    if len(extra_pkgs) > 0:
        build_args += f" --build-arg EXTRA_PKGS=\"{' '.join(extra_pkgs)}\""

    # ---------------------------------- Sources --------------------------------- #
    additional_sources, additional_preferences = read_sources_and_preferences_files(
        sources
    )
    if additional_sources != "":
        build_args += f' --build-arg ADDITIONAL_SOURCES="{additional_sources}"'
    if additional_preferences != "":
        build_args += f' --build-arg ADDITIONAL_PREFERENCES="{additional_preferences}"'

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

    common.run(build_cmd, capture_output=False)
