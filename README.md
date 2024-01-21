# DEBPIC: DEbian Build Package In Container
![alt text](./debpic/Documentation/debpic-logo.png "Logo")  
[![debpic](https://github.com/aidan-gallagher/debpic/actions/workflows/debpic.yml/badge.svg)](https://github.com/aidan-gallagher/debpic/actions/workflows/debpic.yml)
# Introduction

See the [man page](./debpic/Documentation/debpic.manpage.md) for more information.


The [Debian wiki](https://wiki.debian.org/SystemBuildTools#Package_build_tools) has a list of similar tools.


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
