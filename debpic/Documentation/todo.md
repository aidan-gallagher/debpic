## TODO

### Features
* Allow dpkg-buildpackage arguments to be specified in config file
* When --no-cache is given then delete volume ccache.
    * docker volume rm ccache_volume
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
* Unlink rather than delete ./local_repository
* VSCode handle already existing .devcontainer file.
* VScode (--vscode) use image which is already built my debpic. 
    * This means vscode doesn't have to build from scratch despite debpic already having built it.
    * This gets around the problem that VSCode doesn't use BUILDKIT (removes /debian/changelog workaround)
    * This ensures always opens latest version (no prompt from VSCode)
    * Don't need to populate build args.
* Split up debpic.py into multiple files.
    * /usr/lib/python3/dist-packages/
* Consider making DEB_BUILD_OPTIONS an argument rather than environment variable.
    * This stops host env accidentally being used in container build.
    * Makes it possible to add options to config file.
* Long wait times when container can't reach private server
    * When not connected to a VPN and trying to reach a private DNS server debpic hangs for a while.
    * Consider reducing apt timeout times.
* Improve CI testing
    * Try building different repositories (especially ones which require private repositories or local_repository)
* Add dockerfile linter (hadolint)
    * clean up errors
    * add hadolint to CI : https://stackoverflow.com/a/62370018/13365272
* Shellcheck for bash completion (Fix and add to CI)
* Fix lintian warnings
* Uninstall fails if trying to uninstall whilst using a docker image that debpic wants to delete.

### Awaiting upstream fix
* Add docker-buildx as a dependency once it's in Debian. Then VSCode will use buildx/buildkit and the Dockerfile will no longer have to copy debian/copyright.
    * https://github.com/microsoft/vscode-remote-release/issues/1409
    * https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1063381 
    * This problem can be mitigated by VSCode launching an image rather than dockerfile.
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.
* Add inline gpg key to vyatta sources (other repo) when we move to debian 12.
* Consider using `--build-context` once docker build > 23 is in Debian.
