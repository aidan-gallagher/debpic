## ToDo:

* Change local installation away from gdebi.
    * gdebi fails when users wants to install 2 debs that depend on each other.
    * Use dpkg -i *.deb | true , apt install --fix, dpkg -i *.deb. The 2nd install won't have exit true on it.
* Consider techiniques to speed up docker build. 
    * https://gist.github.com/reegnz/990d0b01b5f5e8670f78257875d8daa8
    * https://docs.docker.com/build/cache/
* Add example for VSCode build arg when available: https://github.com/microsoft/vscode-remote-release/issues/3545.
* Integrate docker debug-shell when available: https://github.com/docker/buildx/pull/1640.