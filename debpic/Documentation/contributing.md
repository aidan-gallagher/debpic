
## Introduction
Issues and Pull Requests are welcome on [Github](https://github.com/aidan-gallagher/debpic).

## Source Layout
[comment]: <> (Generated using `$ tree --dirsfirst`)

├── __debian/:__ Debian packaging information for debpic.  
├── __debpic/:__ Source code for debpic.  
│   ├── __Documentation/:__  Documentation for debpic  
│   ├── __hooks/:__  Standard scripts to be used with `debpic --hook`  
│   │   └── __gopath:__  Setup go tooling to use debian Go dev packages.  
│   ├── __debpic-completion.bash:__ Bash completion for debpic CLI options.  
│   ├── __debpic.conf:__  Template configuration file for debpic.  
│   ├── __debpic.py:__ Main script  
│   ├── __debpic_test.py:__ Test for main script.   
│   └── __Dockerfile:__ Dockerfile describing container setup.  
├── __checks.mk:__  Makefile to run code quality checks   
├── __developer-packages.txt:__ List of extra tools debpic will install in the container.  
└── __README.md:__ Landing page for debpic repository.  

## Code Quality

This repository uses the following quality checking tools: black, mypy, pytest & lintian. All of these can be invoked locally in the container using
```
make -f checks.mk 
```
Github Actions will run these checks after a PR is opened to ensure they pass.


