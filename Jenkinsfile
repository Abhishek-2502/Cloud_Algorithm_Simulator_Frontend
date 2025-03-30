pipeline {
    agent { label 'cloudsimFrontend' } // Ensure it runs on your slave node

    environment {
        DOCKER_IMAGE = 'flask-cloudsim-app'
        DOCKER_TAG = 'latest'
        CONTAINER_NAME = 'flask-cloudsim-container'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out the source code...'
                    checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    echo 'Stopping and removing existing container if exists...'
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Running Docker container...'
                    sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
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
