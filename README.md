# DEBPIC: DEbian Build Package In Container
![alt text](./debpic/Documentation/debpic-logo.png "Logo")  
[![debpic](https://github.com/aidan-gallagher/debpic/actions/workflows/debpic.yml/badge.svg)](https://github.com/aidan-gallagher/debpic/actions/workflows/debpic.yml)
# Introduction

See the [man page](./debpic/Documentation/debpic.manpage.md) for an introduction and usage instructions.

# Why use debpic
The [Debian wiki](https://wiki.debian.org/SystemBuildTools#Package_build_tools) has a list of similar tools.  

Debpic installs a [dockerfile](./debpic/Dockerfile) containing all the instructions necessary to setup the environment; the dockerfile allows tools such as [Jenkins](./debpic/Documentation/using-with-jenkins.md) and [VSCode](./debpic/Documentation/using-with-vscode.md) to be used within a container.

Debpic is simple to use, has tab completion and good documentation.

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
