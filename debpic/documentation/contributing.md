
## Introduction
Issues and Pull Requests are welcome on [Github](https://github.com/aidan-gallagher/debpic).

## Source Layout
[comment]: <> (Generated using `$ tree --dirsfirst`)

├── __debian/:__ Debian packaging information for debpic.  
├── __debpic/:__ Source code for debpic.  
│   ├── __Documentation/:__  Documentation for debpic  
│   ├── __hooks/:__  Standard scripts to be used with `debpic --hook`.  
│   │   └── __gopath:__  Setup go tooling to use debian Go dev packages.  
│   ├── __python/:__  
│   │   ├── __build.py:__ Functions to build the container.  
│   │   ├── __common.py:__ Miscellaneous functions.  
│   │   ├── __configuration.py:__ Functions to parse arguments.  
│   │   ├── __debpic.py:__  Entry point to debpic.  
│   │   ├── __debpic_test.py:__  Unit tests.  
│   │   ├── __run.py:__   Functions to run the container.  
│   │   └── __vscode.py:__  Functions for VSCode integration.  
│   ├── __debpic-completion.bash:__ Bash completion for debpic CLI options.  
│   ├── __debpic.conf:__  Template configuration file for debpic.  
│   └── __Dockerfile:__ Dockerfile describing container setup.  
├── __checks.mk:__  Makefile to run code quality checks   
├── __developer-packages.txt:__ List of extra tools debpic will install in the container.  
└── __README.md:__ Landing page for debpic repository.  

## Run Debpic From Repo
During development it is useful to be able to run debpic without having to package it and install it. 

To do this you must change the hardcoded path to the Dockerfile to point to the one in the git repository rather than the install one.

Assuming the repository is located at `~/Code/Per/debpic`. Run:
```
sed -i '/--file \/usr\/share\/debpic\/Dockerfile/ s|/usr/share/debpic/Dockerfile|/home/aidan/Code/Per/debpic/debpic/Dockerfile|' ~/Code/Per/debpic/debpic/python/build.py 
```

Then run `~/Code/Per/debpic/debpic/python/main.py`.


## Code Quality

This repository uses the following quality checking tools: black, mypy, pytest & lintian. All of these can be invoked locally in the container using
```
make -f checks.mk 
```
Github Actions will run these checks after a PR is opened to ensure they pass.


