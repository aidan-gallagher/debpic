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
Enter the container in interactive mode
```
debpic --interactive
```

Copy and paste the following commands
```
# Turn off Go modules
go env -w GO111MODULE=off

# Set the path to the location where debian packages install go code
export GOPATH=/usr/share/gocode/

# Check DH_GOPKG is set before progressing
grep -q "^export DH_GOPKG" debian/rules || { echo "Error: DH_GOPKG is not set in the file."; }

# Determine DH_GOPKG
DH_GOPKG=$(grep -Po '(?<=export DH_GOPKG := ).*' debian/rules)

# Create parent directories to DH_GOPKG location.
sudo mkdir -p /usr/share/gocode/src/$DH_GOPKG

# Remove last directory as it will be symbolic linked and if it's not removed ln will complain/
sudo rm -r /usr/share/gocode/src/$DH_GOPKG

# Symbolic link current directory to DH_GOPKG location.
sudo ln -s $(pwd) /usr/share/gocode/src/$DH_GOPKG
```

Now you can run
```
go test ./...
```