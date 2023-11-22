## TODO


### Features
* Add support for DEB_BUILD_OPTIONS.
* Read .sources from repo if it exists. This allows dpkg-buildenv to just work on any branch. Command line arg should override it.
    * Maybe have dpkg-buidenv.config file. Can set everything same as command line args.
    * Options can be in /etc/dpkg-buildenv, ~/.config/dpkg-buildenv and commandline.
    * https://pypi.org/project/jsonmerge/
* Copy over .git config and bash config so dev use all development tools from within the chroot terminal
* Allow installation of 2 local debs that depend on each other.
    * Change local installation away from gdebi.
        * Option 1: Use dpkg -i *.deb | true; apt install --fix; dpkg -i *.deb. The 2nd install won't have exit true on it.
        * Option 2: Use dpkg-scanpackages.
* Test it out on Microsoft Windows - if it works then add Windows packaging to create .msi


### Clean up 
* Ensure package installs easily on other machines
    * Ubuntu 20.04 - Yes
    * Debian 11 - Yes
    * Ubuntu 22.04 - TODO
* Docker requires password 
    * Can docker be run rootless, so user doesn't have to configure no password after initially installing dpkg-buildenv. 
    * Can this use debconf to ask user if they are happy allowing docker to run without a password instead of having postinst script
* Allow docker to run as `sudo` (?)
* Fix lintian warnings
* Add proper man page
* Uninstall fails if trying to uninstall whilst using a docker image that dpkg-buildenv wants to delete.


### Awaiting upstream fix
* Add example for VSCode build arg when available: https://github.com/microsoft/vscode-remote-release/issues/3545.
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.
