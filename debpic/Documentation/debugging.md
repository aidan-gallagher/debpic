# Debugging Issues with debpic

## Known Issues
When using a VPN to connect to a private apt repository some version of docker can have a DNS issue.
It seems like you have to restart docker.service after connecting to the VPN.

## Steps
1. If it was a timeout error then build it again.
    ```
    debpic
    ```
2. Try building without cache.
    ```
    debpic --no-cache
    ```

3. If you have configured private repositories, ensure you can access them.

   3.1. Check if private repos are enabled.
   ```
   cat /etc/debpic/sources.list.d/default.sources
   ```
   3.2 Ensure the value in "URIs:" is accessible.
   ```
   xdg-open http://build-release.eng.vyatta.net:82/Vyatta:/Shipping:/2308/standard/
   ```

4. If Docker can not resolve you private repositories then you can tell it use your private DNS server

   4.1. Edit the service file
   ```
   sudo systemctl edit docker.service
   ```
   4.2. Add --dns <dns server> to Exec Start
   ```
   [service]
   ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --dns 10.156.16.35 --dns 10.156.16.34
   ```

   4.3. Restart Docker
   ```
   sudo systemctl restart docker.service
   ```

   4.4. If that doesn't work then you could try changing the sources to refer to the build server by IP address rather than domain name.

      ```
      nano /etc/debpic/sources.list.d/default.sources
      ```
      ```
      # Existing
      ...
      URIs: http://build-release.eng.vyatta.net:82/Vyatta:/Unstable/standard/
      ...

      # Replace
      ...
      URIs: http://10.156.50.150:82/Vyatta:/Unstable/standard/
      ...
      ```


4. Ensure the command line arguments look correct.
   ```
   INFO:root:Docker build command: DOCKER_BUILDKIT=1 docker image build --tag vyatta-dataplane-buildenv --file /usr/share/debpic/Dockerfile --network host --build-arg UID=$(id -u) --no-cache --build-arg UID="1000" .
   ```

5. Restart Docker (Not sure how much this helps).
   ```
   sudo systemctl restart docker.service
   ```

6. Enter the container just before the failed layer.

   6.1. Remove `DOCKER_BUILDKIT=1` from build command and run it.
   ```
   docker image build --tag ...
   ```
   6.2. Determine layer hash before fail.
   ```
   Removing intermediate container 2de61280ed82
   ---> ab3e3d73c4e9
   ```
   6.2. Enter layer before it fails.
   ```
   docker run --mount type=bind,src=${PWD},dst=/workspaces/code --user $(id -u):$(id -g) --network host --rm --interactive --tty <CONTAINER_HASH>
   ```


