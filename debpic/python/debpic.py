#!/usr/bin/env python3


import logging
import os
import subprocess
import sys
import yaml
from typing import List

import common
import build
import run
import configuration
import vscode

logging.basicConfig(level=logging.INFO, format="%(message)s")


def main(argv: List[str]):
    try:
        args = configuration.debpic_parse_args(argv)

        if args.delete_images:
            common.delete_images()
            sys.exit()

        build_arguments = build.get_build_arguments(
            args.distribution, args.sources, args.extra_pkg
        )
        if args.get_build_arguments:
            print(build_arguments)
            sys.exit()

        common.prerequisite_check()
        repository_name = common.generate_image_name()

        if args.no_cache == "--no-cache":
            common.run("docker volume rm debpic_cache", check=False)

        with build.hardlink_local_repository(args.local_repository):
            with build.copy_hook(args.hook):
                build.build_image(repository_name, args.no_cache, build_arguments)

        if args.vscode:
            vscode.vscode(repository_name)
            sys.exit(0)

        run.run_container(
            repository_name, args.command, args.dpkg_buildpackage_args, args.interactive
        )

        if args.destination:
            run.move_built_packages(args.destination)

    except KeyboardInterrupt:
        run.kill_container(repository_name)
        sys.exit(130)


if __name__ == "__main__":
    main(sys.argv[1:])
