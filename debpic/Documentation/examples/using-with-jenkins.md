# Jenkins Integration

## Steps
* On the Jenkins server:  
    1.  Install debpic.  
    It will install the Dockerfile to /usr/share/debpic/Dockerfile.
    ```
    sudo apt install ./debpic_1.0.0_all.deb
    ```
    

* In the code repository:  
    1. In the Jenkinsfile reference the installed Dockerfile by adding the following:
    ```
        agent {
            dockerfile {
                filename '/usr/share/debpic/Dockerfile'
            }
        }
    ```
    2. Add Any additional checking tools (e.g mypy, flake8) to ./developer_packages.txt 

    3. Optionally, if you have additional APT repositories:  

        * 2.1 Add the sources to `/etc/debpic/sources.list.d/default.sources`

        * 2.2. Add the following to the top of your Jenkinsfile.
            ```
            node {
                additional_build_args = sh(returnStdout: true, script: 'debpic --get-build-arguments').trim()
            }
            ```
        * 2.3. Add the following under dockerfile
            ```
            additionalBuildArgs "${additional_build_args}"
            ```


The final Jenkinsfile will look something like this
```
node {
    additional_build_args = sh(returnStdout: true, script: 'debpic --get-build-arguments').trim()
}

pipeline {

    agent {
        dockerfile {
            filename '/usr/share/debpic/Dockerfile'
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
