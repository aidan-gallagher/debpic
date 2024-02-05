## TODO

### Features
* Add support for ccache
    * https://askubuntu.com/questions/470545/how-do-i-set-up-ccache
    * mount ~/.cache
    * PATH=/usr/lib/ccache:$PATH DEB_BUILD_OPTIONS="no_lto" dpkg-buildpackage -b
    * When -no-cache option is given then delete ccache too
* Consider adding VSCode flag 
    * Checks installations are good. Maybe try then catch if these go wrong.
        * VSCode exists
        * Devcontainers extension is installed. 
            * "code --install-extension ms-vscode-remote.remote-containers"
        * Devcontainers CLI is installed
    * If .devcontainer file doesn't exist then, 
        * produce a .devcontainer file with correct build arguments
    * Calls vscode devcontainer CLI to open the project.
        * ~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/cli-bin/devcontainer open .
    * If .devcontainer was created  on this run then delete it.
* Add option to change the build program from dpkg-buildpackage to debuild, git-buildpackage, others?
* Add support for signing builds with a key. How best to share a key on the host with the container.
* All the user to specify a post_create_hook that can run any arbitrary setup in the container. Maybe a pre_create_hook too? 
* Consider other environment variables (than DEB_BUILD_OPTIONS) that should be passed through.
    * Are there any other DEB_ or DH_ env variables?
* Copy over .git config and bash config so dev use all development tools from within the chroot terminal
* Test installation of 2 local debs that depend on each other.
* Test debpic out on Microsoft Windows - if it works then add Windows packaging to create .msi
* Performance: Can anything be done to speed up building the container?

### Clean up 
* Split up debpic.py into multiple files.
    * /usr/lib/python3/dist-packages/
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
* Consider using `--build-context` once docker build > 23 is in Debian.
