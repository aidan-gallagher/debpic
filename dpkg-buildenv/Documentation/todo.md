## TODO


### Features
* Add Github Actions. Test on different operating systems
* Add support for DEB_BUILD_OPTIONS.
* Add easy support for passing flags to dpkg-buildpackage.
* Add support for choosing which host os / debian version to use. Maybe make it build argument.
* Have user & repo settings for sources & developer-packages.
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
* Use debconf to ask the user if they want to add ./built_packages to their global git ignore (?)


### Clean up 
* Add dockerfile linter (hadolint)
    * clean up errors
    * add hadolint to CI : https://stackoverflow.com/a/62370018/13365272
* Shellcheck for bash completion (Fix and add to CI)
* Docker requires password 
    * Can docker be run rootless, so user doesn't have to configure no password after initially installing dpkg-buildenv. 
    * Can this use debconf to ask user if they are happy allowing docker to run without a password instead of having postinst script? 
* Allow docker to run as `sudo` (?)
* Fix lintian warnings
* Add proper man page
* Uninstall fails if trying to uninstall whilst using a docker image that dpkg-buildenv wants to delete.
* gdebi shouldn't just install .debs in repo. The user should have to specify it on the command line.

# dpkg-buildenv-vyatta-config 
* If there is no output from "osc ls" then don't write to file.
* Fix cache file so a cron job / systemd updates it rather than on tab completion.

### Awaiting upstream fix
* Add example for VSCode build arg when available: https://github.com/microsoft/vscode-remote-release/issues/3545.
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.
* Add inline gpg key to vyatta sources (other repo) when we move to debian 12.
