# Using with VSCode

1. Install VSCode.

2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
```
ext install ms-vscode-remote.remote-containers
```
3. Create a file named `.devcontainer` in your project's top level directory.

4. Add the following to the file.
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




For more help look at VSCode documentation on [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers).