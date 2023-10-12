# Debugging Issues with dpkg-buildenv

## Docker build issues
1. If it was a timeout error then build it again.
    ```
    dpkg-buildenv
    ```
2. Try building without cache.
    ```
    dpkg-buildenv --no-cache
    ```

1. If you have configured private repositories, ensure you can access them.

   1.1. Check if private repos are enabled.
   ```
   cat /etc/dpkg-buildenv/sources.list.d/default.sources
   ```
   1.2 Ensure the value in "URIs:" is accessible.
   ```
   xdg-open http://build-release.eng.vyatta.net:82/Vyatta:/Shipping:/2308/standard/
   ```

2. Ensure the command line arguments look correct.
   ```
   INFO:root:Docker build command: DOCKER_BUILDKIT=1 docker image build --tag vyatta-dataplane-buildenv --file /usr/share/dpkg-buildenv/Dockerfile --network host --build-arg UID=$(id -u) --no-cache --build-arg UID="1000" .
   ```

3. Restart Docker (Not sure how much this helps).
   ```
   sudo systemctl restart docker.service
   ```

3. Enter the container just before the failed layer.

   3.1. Remove `DOCKER_BUILDKIT=1` from build command and run it.
   ```
   docker image build --tag ...
   ```
   3.2. Determine layer hash before fail.
   ```
   Removing intermediate container 2de61280ed82
   ---> ab3e3d73c4e9
   ```
   3.2. Enter layer before it fails.
   ```
   docker run --mount type=bind,src=${PWD},dst=/workspaces/code --user $(id -u):$(id -g) --network host --rm --interactive --tty <CONTAINER_HASH>
   ```


