# mk-build-deps

Prefer to build the *build-deps*.deb and install it as two seperate commands rather than combining it into once (`mk-build-deps --install --remove  /tmp/control`).

As two seperate commands, if it fails, you are informed of which packages it failed to install. When it is combined you do not see this information.
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