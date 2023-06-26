# Using With Jenkins


Install dpkg-buildenv on the Jenkins server.
```
sudo dpkg -i ./dpkg-buildenv_1.0.0_all.deb
```
It will store the Dockerfile in /opt/dpkg-buildenv.


In the Jenkinsfile reference the installed Dockerfile by adding the following.
```
    agent {
        dockerfile {
            filename '/usr/share/dpkg-buildenv/Dockerfile'
        }
    }
```

The Jenkinsfile will look something like this
```
pipeline {

    agent {
        dockerfile {
            filename '/usr/share/dpkg-buildenv/Dockerfile'
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
