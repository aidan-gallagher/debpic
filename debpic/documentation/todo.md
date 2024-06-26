## TODO
Gradually moving todo's to github issues. 
https://github.com/aidan-gallagher/debpic/issues

### Features
* Add --update-only flag (?)
    * Some users have a workflow where they have --local-repository and --destination as the same directory. They can then build multiple repositories that depend on each other and the local dependency changes will be updated in the parent repository. 
    * Currently this model doesn't work well with debpic as each time debpic is invoked it will write to the --destination which will change the --local-repository directory which will result in the docker image being rebuilt on subsequent runs which while take a good bit of time.
    * Solution: allow --update-only flag which will not rebuild the image but it will run apt update && apt upgrade and then write the image.

    * Workflow explained
        1. Run debpic as normal once to create image
            * If --update-only is specified but no image exists then give warning and ignore flag.
        2. Update dependencies through remote apt server or --local-repository
        3. Run debpic --update-only. Under the hood this will:
            * Skip the "docker build" stage and go to "docker run" (without the --rm flag?)
            * "Docker run" will mount the --local-repository to /tmp/local_repository.
            * Within the container it will run "sudo apt update && sudo apt upgrade"
            * docker commit container_ID image_ID
            * docker rm container
        4. subsequent runs will have to use "--update-only" too otherwise they will call "docker build" which may take some time and will overwrite the existing image.

* DEB environment variables
    * Support all DEB_ and DH_ environment variables (not just DEB_BUILD_OPTIONS)
    * Consider making DEB_BUILD_OPTIONS an argument rather than environment variable.
        * This stops host env accidentally being used in container build.
        * Makes it possible to add options to config file.

* Add --tech-support (hidden option)
    * When dealing with user issues I usually have to ask them run several commands on their machine
    * --tech-support will generate a (zipped?) file with all the info I need
    * debpic version, docker version, /etc/debpic/* files, ~/.config/debpic/* files, is current user part of docker group, can host machine reach private repos in sources, output from the build log, etc.

* Test installation of 2 local debs that depend on each other.

* Performance: Can anything be done to speed up building the container?
    * Maybe a build time mount cache? 
    * https://depot.dev/blog/how-to-use-buildkit-cache-mounts-in-ci

* debconf: Use debconf to ask user if want to run docker without sudo 
    * http://www.fifi.org/doc/debconf-doc/tutorial.html
    * Not necessary if move to podman

* Improve interactive mode development by copying user config files like .git and bash config
    * Should mount (as read only) ~/.config during run time? mount bash files too? Or mount all of $HOME?

* Test debpic out on Microsoft Windows - if it works then add Windows packaging to create .msi

### Clean up 
* Split up debpic.py into multiple files.
    * /usr/lib/python3/dist-packages/

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

### Awaiting upstream fix
* Podman: Consider using podman instead of docker.
    Blocked until move to deb12 as need this feature: https://stackoverflow.com/questions/77619338/conditional-copy-add-in-podman-file

* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.

* Consider using `--build-context` once docker build > 23 is in Debian.

