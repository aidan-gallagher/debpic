## TODO


### Features
* dpkg-buildenv-vyatta-config: Create script to generate sources.file based off of obs project name.
* Add support for DEB_BUILD_OPTIONS.
* Read .sources from repo if it exists. This allows dpkg-buildenv to just work on any branch. Command line arg should override it.
    * Maybe have dpkg-buidenv.config file. Can set everything same as command line args.
    * Options can be in /etc/dpkg-buildenv, ~/.config/dpkg-buildenv and commandline.
    * https://pypi.org/project/jsonmerge/
* Test it out on Microsoft Windows - if it works then add Windows packaging to create .msi

### Clean up
* Use debconf to ask user if they are happy allowing docker to run without a password instead of having postinst script
* Allow easy install on Ubuntu
    * Follow the steps from https://docs.docker.com/engine/install/ubuntu/
* Commit example additional.sources to users can see example of how to add additional sources using deb822 format and including public key.
* Fix lintian warnings
* Add proper man page
* Uninstall fails if trying to uninstall whilst using a docker image that dpkg-buildenv wants to delete.
* Ctrl-C doesn't really work after `docker run` has started - it sometimes continues on.
* Can docker be run rootless, so user doesn't have to configure no password after initially installing dpkg-buildenv.
* Change local installation away from gdebi.
    * gdebi fails when users wants to install 2 debs that depend on each other.
    * Option 1: Use dpkg -i *.deb | true; apt install --fix; dpkg -i *.deb. The 2nd install won't have exit true on it.
    * Option 2: Use dpkg-scanpackages.


### Awaiting upstream fix
* Add example for VSCode build arg when available: https://github.com/microsoft/vscode-remote-release/issues/3545.
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.