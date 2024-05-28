import os
import subprocess

import build
import common
import run


class Test:
    def setup_method(self, test_method):
        # This method is called before every test_* function.
        # It monkey patches the process calls subprocess.check_output()/run().
        # Instead of running these commands as a process they are logged in self.cli_commands.
        self.cli_commands = []

        def run_mock(command, **kwargs):
            self.cli_commands.append(command)
            return "test"

        common.run = run_mock

        def get_uid_mock():
            return 1000

        common.get_uid = get_uid_mock

        def get_env_var_mock(_, default_value):
            return default_value

        os.environ.get = get_env_var_mock

    def test_delete_images(self):
        common.delete_images()
        assert (
            self.cli_commands.pop(0)
            == "docker images '*buildenv' --format {{.Repository}}"
        )
        assert (
            self.cli_commands.pop(0)
            == "docker rmi --force test; docker image prune --force"
        )
        assert self.cli_commands.pop(0) == "docker volume rm debpic_cache"

    def test_build_image(self):
        build.build_image("test_name")
        assert (
            self.cli_commands.pop(0)
            == "DOCKER_BUILDKIT=1 docker image build --tag test_name --file /usr/share/debpic/Dockerfile --network host   ."
        )

        build.build_image("test_name", "--no-cache")
        assert (
            self.cli_commands.pop(0)
            == "DOCKER_BUILDKIT=1 docker image build --tag test_name --file /usr/share/debpic/Dockerfile --network host --no-cache  ."
        )

    def test_run_container(self):
        run.run_container("test_name")
        assert (
            self.cli_commands.pop(0)
            == "docker run --mount type=bind,src=${PWD},dst=/workspaces/code --mount type=volume,src=debpic_cache,dst=/home/docker/.cache --user 1000:$(id -g 1000) --network host --tty --rm --env DEB_BUILD_OPTIONS=\"\"  test_name /bin/bash -c 'if [[ -x /usr/bin/hook ]]; then /usr/bin/hook; fi && dpkg-buildpackage  && mv-debs && dpkg-buildpackage --target=clean'"
        )

        run.run_container("test_name", "echo I'm a test command")
        assert (
            self.cli_commands.pop(0)
            == "docker run --mount type=bind,src=${PWD},dst=/workspaces/code --mount type=volume,src=debpic_cache,dst=/home/docker/.cache --user 1000:$(id -g 1000) --network host --tty --rm --env DEB_BUILD_OPTIONS=\"\"  test_name /bin/bash -c 'if [[ -x /usr/bin/hook ]]; then /usr/bin/hook; fi && echo I'm a test command'"
        )

        run.run_container("test_name", "", "", "--interactive")
        assert (
            self.cli_commands.pop(0)
            == 'docker run --mount type=bind,src=${PWD},dst=/workspaces/code --mount type=volume,src=debpic_cache,dst=/home/docker/.cache --user 1000:$(id -g 1000) --network host --tty --rm --env DEB_BUILD_OPTIONS="" --interactive test_name '
        )
