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
                script {
                    cfDeploy {
                        credentialsId = "${this.env.CREDS}"
                        org = "${this.env.ORG}"
                        space = "${this.env.SPACE}"
                        manifestPath = "/manifest.yml"
                    }
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
            echo 'Successful'
        }
        unstable {
            echo 'Unstable'
        }
        failure {
            echo 'Failed'
        }
    }
}