# Debian Package Build Environment (dpkg-buildenv)
## Introduction
dpkg-buildenv lets you build Debian packages in an isolated Docker environment. The environment is composed from:
* The [Debian stable docker image](https://hub.docker.com/_/debian/)
* Build dependencies describered in Build-Depends section of <repository_name>/debian/control
* Any additional developer tools described in <repository_name>/developer-packages.txt.

The isolated Docker enviornment is good because:
* There isn't a risk that the dependencies will break you host OS.
* It is easy to set up  - so new developers can get up to speed quickly.
* It is provides a consistent environment for the developers and the continuous integration system.

The [Debian wiki](https://wiki.debian.org/SystemBuildTools#Package_build_tools) has a list of similar tools.

## Usage

### Building a package
1. Clone the repository you want to build
```
$ https://salsa.debian.org/apt-team/apt.git
```

2. Run dpkg-buildenv
```
$ dpkg-buildenv
```

3. Find your newly created debian packages
```
$ ls ./built_packages
```

### Running a command inside the container
```
$ dpkg-buildenv '<your_command_to_run>'

$ dpkg-buildenv 'echo Hi I'm inside the container. See the output of whoami command; whoami'
```
### Entering the contianer via the CLI
```
$ dpkg-buildenv --interactive-tty
```

### Deleting images
This tool creates a docker image for every repository. To remove them run:
```
$ dpkg-buildenv --delete-images
```

### Using With Other Tools
See documentantion how to use with [Jenkins](./Documentation/using-with-jenkins.md) and [VSCode](./Documentation/using-with-vscode.md).

## Design

The implementation of this program is fairly simple; if are familiar with Python, Docker and Debian packaging then you should understand it fairly easily (within ~15 minutes).  

The [dockerfile](./Dockerfile) contains the instructions to create the containised enviornment.  
* It sets up the docker user.
* It adds the private apt repositories.
* It changes the parent directory permissions.
* It copies over the debian/control file from the repository.
* It optionally copies over the developer-packages.txt file from the repository if it exists.
* It uses mk-build-deps to install all the dependencise in the Build-Depends section of the debian/control file.
* It installs all the dependencise in the devleper-packages.txt file.

The [dpkg-buildenv.py](./dpkg-buildenv.py) script handles the user command line options and invokes Docker.
* It finds the current folder's name and uses that as the image name.
* It builds the Docker image.
* It runs the Docker image.
* It calls dpkg-buildpackage within the container to build the package.

# Installation

You must allow docker to run as non-root user. To do this follow the steps in the [official docker documentation](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).