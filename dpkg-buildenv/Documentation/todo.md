## ToDo:

* Check private repos are reachable
    * RUN apt-get update 2>&1 >/dev/null || (echo Fix Apt warning before progressing; exit 1)
    * https://askubuntu.com/questions/74345/how-do-i-bypass-ignore-the-gpg-signature-checks-of-apt
* Allow user to specify apt priority for different repos
* Consider techiniques to speed up docker build. 
    * https://gist.github.com/reegnz/990d0b01b5f5e8670f78257875d8daa8
    * https://docs.docker.com/build/cache/
* Integrate this when it becomes available (Probably a long time away) https://github.com/docker/buildx/pull/1640.