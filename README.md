# DEBPIC: DEbian Build Package In Container
![alt text](./debpic/Documentation/debpic-logo.png "Logo")  
[![debpic](https://github.com/aidan-gallagher/debpic/actions/workflows/debpic.yml/badge.svg)](https://github.com/aidan-gallagher/debpic/actions/workflows/debpic.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/aidan-gallagher/debpic/graph/badge.svg?token=G0WWQPPIIC)](https://codecov.io/gh/aidan-gallagher/debpic)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
# Introduction

Debpic lets you build Debian packages in an isolated Docker environment.

See the [man page](./debpic/Documentation/debpic.manpage.md) for an introduction and usage instructions.

The [Debian wiki](https://wiki.debian.org/SystemBuildTools#Package_build_tools) has a list of similar tools.  
# Overview

| Tasks                                   | Steps                                                               |
|-----------------------------------------|---------------------------------------------------------------------|
| Build                                   | `debpic`                                                            |
| Interactive mode                        | `debpic --interactive`                                              |
| Open VSCode in container                | `debpic --vscode`                                                   |
| Local Apt Repository                    | `debpic --local-repository ~/mydebs`                                |
| Private Apt Repository (Configure)      | Write deb822 format sources to `/etc/debpic/sources.list.d/MyServer`|
| Private Apt Repository (Use)            | `debpic --sources MyServer`                                         |
| Use DEB_BUILD_OPTIONS                   | `DEB_BUILD_OPTIONS="nocheck no_lto" debpic`                         |
| Run Command in container                | `debpic "my command"`                                               |
| Install extra packages                  | `debpic --extra-pkg gdb`                                            |
| Set destination directory               | `debpic --destination ~/my_built_packages`                          |
| Pass args to dpkg-buildpackage          | `debpic -- -b`                                                      |
| Hook script (Configure)                 | Write script to `/etc/debpic/hooks/myscript`                        |
| Hook script (Use)                       | `debpic --hook myscript`                                            |
| Use golang tooling                      | `debpic --hook gopath --interactive`                                |
| Jenkins Integration                     | See [Using With Jenkins](debpic/Documentation/using-with-jenkins.md). |


| User Experience                         | Info                                                                |
|-----------------------------------------|---------------------------------------------------------------------|
| Tab completion                          | Yes                                                                 |
| Man page                                | Yes                                                                 |
| Coloured Output                         | Yes                                                                 |
| Caching                                 | Container is cached. Ccache enabled by default.                     |
| Config file                             | `~/.config/debpic/debpic.conf`                                      |
| Built package location                  | `./built_packages/`                                                 |
| Include extra tools                     | Edit ./developer-packages.txt                                       |

# Installation

1. Download [debpic debian package]( 
https://github.com/aidan-gallagher/debpic/releases/download/v1.0.0/debpic_1.0.0_all.deb)

2. Install debpic
```
sudo apt install ~/Downloads/debpic_1.0.0_all.deb
```

3.  Configure docker to run as non-root user. See [official docker documentation](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) for more details.
```
sudo usermod -aG docker $USER
newgrp docker
```
4. . Optionally - configure git to globally ignore generated built_packages directory
```
echo built_packages >> ~/.config/git/ignore
```

# Documentation

For more information see the [documentation](debpic/Documentation).

