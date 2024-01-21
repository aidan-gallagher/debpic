## TODO

### Bugs
* ./local_packages are ignored when the container is setup using devcontainers with VSCode.


### Features
* Consider other environment variables (than DEB_BUILD_OPTIONS) that should be passed through.
    * Are there any other DEB_ or DH_ env variables?
* Add easy support for passing flags to dpkg-buildpackage.
* Allow multiple config files? Setting from commandline, <REPO>/debpic.conf, ~/.config/debpic/config.conf then /etc/debpic/config.conf
* Copy over .git config and bash config so dev use all development tools from within the chroot terminal
* Test installation of 2 local debs that depend on each other.
* Test debpic out on Microsoft Windows - if it works then add Windows packaging to create .msi
* Use debconf to ask the user if they want to add ./built_packages to their global git ignore (?)


### Clean up 
* Add dockerfile linter (hadolint)
    * clean up errors
    * add hadolint to CI : https://stackoverflow.com/a/62370018/13365272
* Shellcheck for bash completion (Fix and add to CI)
* Fix lintian warnings
* Uninstall fails if trying to uninstall whilst using a docker image that debpic wants to delete.

### Awaiting upstream fix
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.
* Add inline gpg key to vyatta sources (other repo) when we move to debian 12.
