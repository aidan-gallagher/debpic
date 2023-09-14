# Using with VSCode


1. Install dpkg-buildenv.
```
sudo dpkg -i ./dpkg-buildenv_1.0.0_all.deb
```
It will store the Dockerfile in /usr/share/dpkg-buildenv/.

2. Install VSCode.

3. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) by launching VSCode Quick Open (`Ctrl + P`) and paste.
```
ext install ms-vscode-remote.remote-containers
```
4. Create a file named `.devcontainer` in your project's top level directory amd add the following:

```
{
	"name": "Code Build Environment",

	"dockerFile": "/usr/share/dpkg-buildenv/Dockerfile",

	"remoteUser": "docker",

	// Add the IDs of extensions you want installed in the container
	"customizations": {
		"vscode": {
			"extensions": [
				"eamodio.gitlens",
				"alefragnani.Bookmarks",
			]
		}
	}	
}
```
5. Open the command pallet (Ctrl + Shift+ P) and paste:
```
Dev Containers: Reopen in Container
```



For more help look at VSCode documentation on [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers).