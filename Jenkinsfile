#!groovy

@NonCPS
def cancelPreviousBuilds() {
    def jobName = env.JOB_NAME
    def buildNumber = env.BUILD_NUMBER.toInteger()
    // Get job name
    def currentJob = Jenkins.instance.getItemByFullName(jobName)

    // Iterating over the builds for specific job
    for (def build : currentJob.builds) {
        // If there is a build that is currently running and it's not current build
        if (build.isBuilding() && build.number.toInteger() != buildNumber) {
            // Than stopping it
            build.doStop()
        }
    }
}

pipeline {

    agent {
        dockerfile true
    }

    options {
        quietPeriod(30) // Wait in case there are more SCM pushes/PR merges coming
        ansiColor('xterm')
    }

    stages {

        // A work around, until this feature is implemented: https://issues.jenkins-ci.org/browse/JENKINS-47503
        stage('Cancel older builds') { steps { script {
            cancelPreviousBuilds()
        }}}

        stage('Package') {
            steps {
                sh "dpkg-buildpackage"
            }
        }

        stage('Lintian') {
            steps {
                sh "lintian --fail-on warning"
            }
        }

        stage('Black') {
            steps {
                sh "black --check ."
            }
        }

        stage('PyTest') {
            steps {
                sh "pytest-3 "
            }
        }
    }
}