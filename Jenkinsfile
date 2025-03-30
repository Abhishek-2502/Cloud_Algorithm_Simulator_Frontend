pipeline {
    agent { label 'cloudsimFrontend' }

    environment {
        DOCKER_IMAGE = 'flask-cloudsim-app'
        DOCKER_TAG = 'latest'
        CONTAINER_NAME = 'flask-cloudsim-container'
        SSH_CREDENTIALS_ID = 'cloudsim-frontend-slave' // Use the ID of the SSH credential
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out code using SSH with private repo access...'
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'git@github.com:YourUsername/YourPrivateRepo.git', // Use SSH URL
                            credentialsId: "${SSH_CREDENTIALS_ID}"
                        ]]
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Stop and Remove Existing Container') {
            steps {
                script {
                    echo 'Stopping and removing any existing container with the same name...'
                    sh "docker ps -a -q --filter 'name=${CONTAINER_NAME}' | xargs -r docker stop"
                    sh "docker ps -a -q --filter 'name=${CONTAINER_NAME}' | xargs -r docker rm"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                echo 'Running new Docker container...'
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed. Please check the logs.'
        }
    }
}
