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
#12 2.091  <PACKAGE_1>                  : Depends: <PACKAGE_2> but it is not installable
#12 2.091                                 Depends: <PACKAGE_3> but it is not installable
#12 2.091                                 Depends: <PACKAGE_4> but it is not installable
#12 2.091                                 Depends: <PACKAGE_5> but it is not installable
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
--build-arg ADDITIONAL_SOURCES="Enabled: Yes\nTypes: deb\nURIs: http://my_apt_repo/Debian11/\nSuites: ./\nTrusted: yes\n\n.
```
We could COPY the file from `/etc/debpic/sources.list.d/` instead.

## Buildkit's "RUN --mount" vs copying at built time

Whenever the local_repository is updated then the docker container has to be rebuilt. That is ok but it might be preferable to avoid that because:
* Whenever remote apt repositories are updated the docker container isn't forced to update
* If the user specifies the same directory for --local-repository and --destination then the container is always rebuilt.

### Attempt 1
Instead of copying files at build time they can be mounted using the following syntax:
```
RUN --mount=type=bind,source=/local_repository,target=/tmp/local_repository \
    ls /tmp/local_repository > /tmp/hi
```

The root of source is the build context (where docker build was invoked) for example ~/Code/debpic rather than the root of the host machine. That is fine as that is the same as how COPY works

This works when local_repository folder exists. The trouble is that directory is optional.

### Attempt 2
An idea is to make the local_repository a variable. The python checks if it exists and then sets LOCAL_REPO build arg during build time, and if it doesn't exist then LOCAL_REPO is just to "" or /debian since that's guaranteed to exist.

```
ARG LOCAL_REPO="/local_repository"
RUN --mount=type=bind,source=$LOCAL_REPO,target=/tmp/local_repository \
    ls /tmp/local_repository > /tmp/hi
```

Unfortunately this fails because docker treats the variable as a cache key rather than the path on host OS :(
```
 => CACHED [ 8/17] RUN apt-get update &&     apt-get install devscripts equivs apt-utils ccache                                              0.0s
 => ERROR [ 9/17] RUN --mount=type=bind,source=/local_repository,target=/tmp/local_repository     ls /tmp/local_repository > /tmp/hi         0.0s
------
 > [ 9/17] RUN --mount=type=bind,source=/local_repository,target=/tmp/local_repository     ls /tmp/local_repository > /tmp/hi:
------
failed to compute cache key: "/$LOCAL_REPO" not found: not found
```

## Attempt 2.5
Attempt 2 issue has a bug: This is documented here: https://github.com/moby/buildkit/issues/815

Adding the following to the top of file works.
```
# syntax = docker/dockerfile:latest
```

If I change the contents of the local_directory then it triggers rebuild. This is the same behaviour as COPY so there is no point going down this direction.


### Attempt 3

Using mount type as volume is not allowed
```
RUN --mount=type=volume,source=debpic_cache,target=/tmp/local_repository \
    ls /tmp/local_repository > /tmp/hi
```
```
failed to solve with frontend dockerfile.v0: failed to create LLB definition: dockerfile parse error line 80: unsupported mount type "volume"
```

