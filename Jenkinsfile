pipeline {
    agent { label 'cloudsimFrontend' }

    environment {
        DOCKER_IMAGE = 'flask-cloudsim-app'
        DOCKER_TAG = 'latest'
        CONTAINER_NAME = 'flask-cloudsim-container'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code using preconfigured SCM...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Stop and Remove Existing Container') {
            steps {
                script {
                    sh "docker ps -a -q --filter 'name=${CONTAINER_NAME}' | xargs -r docker stop"
                    sh "docker ps -a -q --filter 'name=${CONTAINER_NAME}' | xargs -r docker rm"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run -d --restart always -p 5000:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:${DOCKER_TAG}"
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
