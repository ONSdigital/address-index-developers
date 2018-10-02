pipeline {

    environment {
        SVC_NAME = "address-index-developers"
        ORG = "ai"
    }

    triggers {
        pollSCM('*/5 * * * *')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '8'))
    }

    agent any

    stages {
        stage('Code pull'){
            steps{
                checkout scm
            }
        }

        stage('Deploy') {
            environment {
                CREDS = 'ai_jenkins'
                SPACE = 'dev'
            }
            steps {
                cfPush {
                    organization: '${this.env.ORG}',
                    cloudSpace: '${this.env.SPACE}',
                    credentialsId: '${this.env.CREDS}'
                    manifestPath = '/manifest.yml'
                }
            }
            post {
                success {
                    colourText("info", "Stage: ${env.STAGE_NAME} successful!")
                }
                failure {
                    colourText("warn", "Stage: ${env.STAGE_NAME} failed!")
                }
            }
        }

    }
    post {
        success {
            colourText("success", "All stages complete. Build was successful.")
        }
        unstable {
            colourText("warn", "Something went wrong, build finished with result ${currentResult}. This may be caused by failed tests, code violation or in some cases unexpected interrupt.")
        }
        failure {
            colourText("warn", "Process failed at: ${env.NODE_STAGE}")
        }
    }
}