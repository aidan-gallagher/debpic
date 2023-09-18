# Using With Jenkins


1. Install dpkg-buildenv on the Jenkins server.
```
sudo dpkg -i ./dpkg-buildenv_1.0.0_all.deb
```
It will store the Dockerfile in /usr/share/dpkg-buildenv/.


2. In the Jenkinsfile reference the installed Dockerfile by adding the following.
```
    agent {
        dockerfile {
            filename '/usr/share/dpkg-buildenv/Dockerfile'
        }
    }
```
Optionally, if you have additional repositories:  

3. Add the sources to `/etc/dpkg-buildenv/sources.list.d/default.sources`

4. Add the following to the top of your Jenkinsfile.
```
node {
    additional_build_args = sh(returnStdout: true, script: 'dpkg-buildenv --get-build-arguments').trim()
}
```
5. Add the following under dockerfile
```
additionalBuildArgs "${additional_build_args}"
```


The Jenkinsfile will look something like this
```
node {
    additional_build_args = sh(returnStdout: true, script: 'dpkg-buildenv --get-build-arguments').trim()
}

pipeline {

    agent {
        dockerfile {
            filename '/usr/share/dpkg-buildenv/Dockerfile'
            additionalBuildArgs "${additional_build_args}"
        }
    }

 stages {
    stage('Static Analysis') {
        steps {
            sh "flake8 ."
        }
    }
    stage('Package') {
        steps {
            sh "dpkg-buildpackage"
        }
    }
    ...
```

For more help look at Jenkins documentation on [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/) and [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/).
