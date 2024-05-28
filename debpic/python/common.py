import logging
import os
import subprocess


def run(cmd: str, capture_output=True, check=True) -> str:
    if capture_output == False:
        green_txt_start = "\033[92m"
        bold_txt_start = "\033[1m"
        fmt_txt_end = "\033[0m"
        logging.info(
            f"{bold_txt_start}{green_txt_start}Running command:{fmt_txt_end} {green_txt_start}{cmd}{fmt_txt_end}"
        )
    return subprocess.run(
        cmd, shell=True, text=True, capture_output=capture_output, check=check
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
        run(f"docker rmi --force {find_result}; docker image prune --force")
    else:
        logging.info("No images to delete")

    run("docker volume rm debpic_cache", check=False)


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
