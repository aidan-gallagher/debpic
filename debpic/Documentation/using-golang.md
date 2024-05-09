# Introduction
Go modules are the recommended method for handling dependencies, however, debian packaging uses GOPATH instead.

# Benefits
The benefits I see to using the Debian packing / go path workflow over go modules are:
 
* **Consistent Workflow:** By following the Debian packaging approach, the workflow remains consistent with other packages written in different languages. For instance, in Python development, we typically install packages using sudo apt install python3-<packageName> rather than pip install <packageName>.
 
* **Single Source for Dependencies:** Dependency information only has to exist in 1 place (debian/control files), rather than debian/control file and go.mod.
 
* **Upstream Version:** The correct upstream dependency version is selected. The Debian package version of tools is usually always different from the version on github.
 
* **Generated Protobufs:** Protobufs which are generated at build time are only available from the debian package and not available using go mod.
 
* **Quilt Patches:** Patches to dependencies are applied in the debian packaged version but not when using go.mod.
 
* **Consistent output:** The generated binary is the same (or more similar) to the one created by the image build system (same OS, golang version, dependencies version).
 
* **Local dependencies:** Changing a dependency and locally including it in another project can done using the existing workflow.
    ```
    debpic --local-repository ~/my_debs
    ```
    
# Steps
Enter the container in interactive mode and invoke the gopath setup script
```
debpic --interactive --hook gopath
```

Now you can run
```
go test ./...
```