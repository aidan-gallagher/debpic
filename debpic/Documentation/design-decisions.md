# Build Time vs Run Time

`debpic` has most of the logic in the Dockerfile.   
An alternative approach is to have little in the dockerfile and then set up the environment with run commands.  
The benefit of doing all the setup in the Dockerfile is that:
* It's easily integrated with tools like Jenkins and VSCode.
* The caching of images is all handled by docker.  

The drawback is the extra complexity of:  
* Conditionally copying files
* Copying files from outwith repository (e.g /etc/debpic/sources/list.d
* Conditionally running certain parts of the Dockerfile.


# mk-build-deps

`mk-build-deps` can generate the package to install the dependencies, install that package and then delete the generate package all with the following single command.
``````
mk-build-deps --install --remove  /tmp/control
``````

I have opted to build the *build-deps*.deb and install it as two separate commands. 
```
mk-build-deps /tmp/control && \
apt-get install ./*build-deps*.deb
```

Two commands is preferred because if it fails then the the user is told which packages failed. For example:
```
...
#12 2.053 
#12 2.053 The following packages have unmet dependencies:
#12 2.091  vplane-config-qos-build-deps : Depends: dh-yang but it is not installable
#12 2.091                                 Depends: dh-vci but it is not installable
#12 2.091                                 Depends: golang-github-danos-vyatta-dataplane-protobuf-dev but it is not installable
#12 2.091                                 Depends: golang-github-danos-vci-dev but it is not installable
#12 2.096 E: Unable to correct problems, you have held broken packages.
```

## --build-context
[Docker supports multiple build contexts](https://www.docker.com/blog/dockerfiles-now-support-multiple-build-contexts/).  
This is in docker build (>23). Unfortunately it not available in Debian.
* Deb11: Docker version 20.10.5       -  Too old
* Deb12: Docker version: 20.10.24   -  Too old
* Ubuntu 20.04: Docker version 24.0.5  - Good for it

If it was then instead of passing 
```
--build-arg ADDITIONAL_SOURCES="Enabled: Yes\nTypes: deb\nURIs: http://10.156.50.45:82/Tools/Debian11/\nSuites: ./\nTrusted: yes\n\nEnabled: Yes\nTypes: deb\nURIs: http://10.156.50.45:82/Vyatta:/Tools/Debian11/\nSuites: ./\nTrusted: yes\n\nEnabled: Yes\nTypes: deb\nURIs: http://10.156.50.150:82/Vyatta:/Unstable/standard/\nSuites: ./\nTrusted: yes\n" .
```
We could COPY the file from `/etc/debpic/sources.list.d/` instead.