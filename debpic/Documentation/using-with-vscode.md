# Using with VSCode


1. Install debpic.
```
sudo dpkg -i ./debpic_1.0.0_all.deb
```
It will store the Dockerfile in /usr/share/debpic/.

2. Install VSCode.

3. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) by launching VSCode Quick Open (`Ctrl + P`) and paste.
```
ext install ms-vscode-remote.remote-containers
```
4. Create a file named `.devcontainer` in your project's top level directory and add the following:

```
{
	"name": "Code Build Environment",

	"dockerFile": "/usr/share/debpic/Dockerfile",

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

5. If you have custom build arguments to pass such as a private APT repo or you are using a different debian version then you need specify the build arguments.

	5.1 Ensure on dev containers is on version v0.330.0 (Pre-Release) or later.

	5.2  Invoke `debpic --get-build-arguments` followed by your chosen arguments.
	```
	debpic --get-build-arguments --sources unstable --distribution debian:12 

	--build-arg UID="1000" --build-arg ADDITIONAL_SOURCES="Enabled: Yes\nTypes: deb\nURIs: http://10.156.50.45:82/Tools/Debian11/\nSuites: ./\nTrusted: yes\n\nEnabled: Yes\nTypes: deb\nURIs: http://10.156.50.45:82/Vyatta:/Tools/Debian11/\nSuites: ./\nTrusted: yes\n\nEnabled: Yes\nTypes: deb\nURIs: http://10.156.50.150:82/Vyatta:/Unstable/standard/\nSuites: ./\nTrusted: yes\n" --build-arg DISTRIBUTION=debian:12
	```
	5.3. Extract and copy the individual build arguments into the `.devcontainer` YAML under build-> args
	```
	{
		...
		"dockerFile": "/usr/share/debpic/Dockerfile",
		
		"build": {
			"args": {
				
				"ADDITIONAL_SOURCES=" : "Enabled: Yes\nTypes: deb\nURIs: http://10.156.50.45:82/Tools/Debian11/\nSuites: ./\nTrusted: yes\n\nEnabled: Yes\nTypes: deb\nURIs: http://10.156.50.45:82/Vyatta:/Tools/Debian11/\nSuites: ./\nTrusted: yes\n\nEnabled: Yes\nTypes: deb\nURIs: http://10.156.50.150:82/Vyatta:/Unstable/standard/\nSuites: ./\nTrusted: yes\n"

				"DISTRIBUTION" : "debian:12"
			}
		},
		...
	```

6. Open the command pallet (Ctrl + Shift+ P) and paste:
```
Dev Containers: Reopen in Container
```

For more help look at VSCode documentation on [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers).