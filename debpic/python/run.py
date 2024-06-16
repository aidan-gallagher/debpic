import os
import subprocess
import sys

import common


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
    # command with "/bin/bash -c" and invoke the hook.
    command = (
        f"/bin/bash -c 'if [[ -x /usr/bin/hook ]]; then /usr/bin/hook; fi && {command}'"
    )

    # If interactive mode is specified then remove any commands
    if interactive != "":
        command = ""

    deb_build_options = os.environ.get("DEB_BUILD_OPTIONS", "")

    # TODO: If the host doesn't have gpg installed then skip this.
    gpg_home = common.run("gpgconf --list-dir homedir").strip()
    gpg_socket = common.run("gpgconf --list-dirs agent-socket").strip()

    run_cmd = f"""\
docker run
--mount type=bind,src=${{PWD}},dst=/workspaces/code
--mount type=volume,src=debpic_cache,dst=/home/docker/.cache
--mount type=bind,src={gpg_socket},dst=/home/docker/.gnupg/S.gpg-agent,readonly
--mount type=bind,src={gpg_home}/pubring.kbx,dst=/home/docker/.gnupg/pubring.kbx,readonly
--mount type=bind,src={gpg_home}/trustdb.gpg,dst=/home/docker/.gnupg/trustdb.gpg,readonly
--user {common.get_uid()}:$(id -g {common.get_uid()})
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
        result = common.run(run_cmd, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"Build failed!")
        sys.exit(e.returncode)


def move_built_packages(destination):
    common.run(f"mkdir --parents {destination}")
    common.run(f"[ ! -d built_packages ] || mv built_packages/*.deb {destination}")
    common.run("rm -rf built_packages/")


def kill_container(repository_name):
    result = common.run(
        f"docker ps --all --quiet --filter ancestor={repository_name}"
    ).replace("\n", " ")
    if result != "":
        common.run(f"docker kill {result}")
