# Build Time vs Run Time

`dpkg-buildenv` has most of the logic in the Dockerfile.   
An alternative approach is to have little in the dockerfile and then set up the environment with run commands.  
The benefit of doing all the setup in the Dockerfile is that:
* It's easily integrated with tools like Jenkins and VSCode.
* The caching of images is all handled by docker.  

The drawback is the extra complexity of:  
* Conditionally copying files
* Copying files from outwith repository (e.g /etc/dpkg-buildenv/sources/list.d
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

