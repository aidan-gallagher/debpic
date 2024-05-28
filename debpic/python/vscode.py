import os
import sys

import common


def vscode(repository_name):
    # ----------------------------- Prerequite check ----------------------------- #
    # Check VSCode
    from shutil import which

    if which("code") is None:
        sys.exit("Please install VSCode first")

    # Check Dev Container
    devcontainer_cli = os.path.expanduser(
        "~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/cli-bin/devcontainer"
    )
    if not os.path.isfile(devcontainer_cli):
        sys.exit(
            "Please install Dev Containers extension for VSCode:  (https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)"
        )

    # --------------- Create .devcontainer file -------------- #

    deb_build_options = os.environ.get("DEB_BUILD_OPTIONS", "")

    devcontainer = f"""
{{
        // This file was automatically generated by debpic. It will be overwritten by subsequent runs of "debpic --vscode."
        "name": "{repository_name}",
        "image": "{repository_name}",
        "mounts": [
            "source=debpic_cache,target=/home/docker/.cache,type=volume",
        ],
        "containerEnv": {{
            "DEB_BUILD_OPTIONS": "{deb_build_options}"
        }},
        "runArgs": ["--hostname", "{repository_name}",
                    "--name", "vscode-{repository_name}",
                    "--rm"],

        "remoteUser": "docker",

        "postStartCommand": "bash -c  'if [[ -x /usr/bin/hook ]]; then /usr/bin/hook; fi'",

        // TODO: allow the user to configure these? Maybe put this file as a template in /etc/debpic ?
        "customizations": {{
                "vscode": {{
                        "extensions": [
                                "eamodio.gitlens",
                                "alefragnani.Bookmarks",
                                "littlefoxteam.vscode-python-test-adapter"
                        ]
                }}
        }}
}}
"""
    # Write .devcontainer if file doesn't already exists or it was generated by debpic.
    if (
        not os.path.exists("./.devcontainer.json")
        or "This file was automatically generated by debpic"
        in open("./.devcontainer.json").read()
    ):
        with open("./.devcontainer.json", "w") as file:
            file.write(devcontainer)

    # ------------------------- Open VSCode in container ------------------------- #
    common.run(
        "~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/cli-bin/devcontainer open ."
    )
