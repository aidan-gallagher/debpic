## TODO

### Bugs
* ./local_packages are ignored when the container is setup using devcontainers with VSCode.


### Features
* Allow local_packages to be specified anywhere on host machine. Either use:
    * --build-context: only available on docker build > 23 (not in debian)
    * Hard links
* Only install local_packages that are referenced in build-depends or developer-packages.txt rather than all of them.
* Add option to change the build program from dpkg-buildpackage to debuild, git-buildpackage, others?
* Add support for signing builds with a key. How best to share a key on the host with the container.
* Add command line flag --extra-pkgs.
    * This means the user can have their user packages for all containers specified in their config file.
    * Bash completion: 
        * Either have a file for ubuntu packages and a file for debian packages and read them depending on what --distribution has been specified.
        * Or use "apt-cache --no-generate pkgnames" Can probably just run this on host machine and it'll be close enough.
    * Install these early in dockerfile as unlikely to change
* Add easy support for passing flags to dpkg-buildpackage.
* Consider other environment variables (than DEB_BUILD_OPTIONS) that should be passed through.
    * Are there any other DEB_ or DH_ env variables?
* Allow multiple config files? Setting from commandline, <REPO>/debpic.conf, ~/.config/debpic/config.conf then /etc/debpic/config.conf
* Copy over .git config and bash config so dev use all development tools from within the chroot terminal
* Test installation of 2 local debs that depend on each other.
* Test debpic out on Microsoft Windows - if it works then add Windows packaging to create .msi
* Use debconf to ask the user if they want to add ./built_packages to their global git ignore (?)


### Clean up 
* Long wait times when container can't reach private server
    * When not connected to a VPN and trying to reach a private DNS server debpic hangs for a while.
    * Consider reducing apt timeout times.
* Add dockerfile linter (hadolint)
    * clean up errors
    * add hadolint to CI : https://stackoverflow.com/a/62370018/13365272
* Shellcheck for bash completion (Fix and add to CI)
* Fix lintian warnings
* Uninstall fails if trying to uninstall whilst using a docker image that debpic wants to delete.

### Awaiting upstream fix
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.
* Add inline gpg key to vyatta sources (other repo) when we move to debian 12.
