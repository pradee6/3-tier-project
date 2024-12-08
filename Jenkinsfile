pipeline {
    agent any

    environment {
        GITHUB_REPO = 'https://github.com/pradee6/3-tier-project.git'
        GITHUB_CREDENTIALS_ID = 'github-key'
        SONARQUBE_SERVER = 'SonarQube Server'
        SONAR_PROJECT_KEY = '3-tier-project'
        DOCKER_CREDENTIALS_ID = 'docker-credentials'
        COMPOSE_FILE = 'docker-compose.yml'
        K8_CREDENTIALS_ID = 'K8_client'  // Reference to your SSH credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: "${GITHUB_CREDENTIALS_ID}", url: "${GITHUB_REPO}"
                sh 'ls -l' // Debug step to confirm files
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL}
                        """
                    }
                }
            }
        }

        stage('Docker Compose Build') {
            steps {
                script {
                    sh "docker-compose -f ${COMPOSE_FILE} build"
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    sh "docker-compose -f ${COMPOSE_FILE} build"

                    def images = sh(
                        script: "docker-compose -f ${COMPOSE_FILE} config | grep 'image:' | awk '{print \$2}'",
                        returnStdout: true
                    ).trim().split("\n")

                    images.each { image ->
                        echo "Scanning image: ${image}"
                        sh """
                            docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            -v \$(pwd):/root/.cache/ \
                            aquasec/trivy image ${image} 
                        """
                    }
                }
            }
        }

        stage('Tag and Push Images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        // Login to Docker Hub (or another registry if needed)
                        sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                    }

                    // Get all image names from the docker-compose file
                    def images = sh(
                        script: "docker-compose -f ${COMPOSE_FILE} config | grep 'image:' | awk '{print \$2}'",
                        returnStdout: true
                    ).trim().split("\n")

                    images.each { image ->
                        def localImage = image.replace("\"", "").trim()

                        // Use the image name as is, without specifying a custom repository.
                        // This assumes you're pushing to the default Docker Hub repository for the logged-in user.
                        def customTag = "${localImage.split(':')[0]}:latest"  // Tag image as latest

                        echo "Tagging and pushing image: ${localImage} as ${customTag}"

                        // Tag the image
                        sh "docker tag ${localImage} ${customTag}"
                        
                        // Push the image to the registry (Docker Hub by default)
                        sh "docker push ${customTag}"
                    }
                }
            }
        }

        stage('Docker Compose Up') {
            steps {
                script {
                    sh "docker-compose -f ${COMPOSE_FILE} up -d"
                }
            }
        }

        stage('K8 Login') {
            steps {
                sshagent([K8_CREDENTIALS_ID]) {
                    // Ensure SSH credentials are configured and work correctly for EC2 access
                    sh 'scp -o StrictHostKeyChecking=no ./k8s-deployment.yaml ec2-user@15.152.41.111:/home/ec2-user/'
                }
            }
        }

        stage('K8 Deployment') {
            steps {
                sshagent([K8_CREDENTIALS_ID]) {
                    // Apply the deployment and service configuration using the correct user and file path
                    sh 'ssh ec2-user@15.152.41.111 "sudo kubectl apply -f /home/ec2-user/k8s-deployment.yaml"'

                    // Restart the deployment to ensure the changes are applied
                    sh 'ssh ec2-user@15.152.41.111 "sudo kubectl rollout restart deployment/web-server"'
                    sh 'ssh ec2-user@15.152.41.111 "sudo kubectl rollout restart deployment/app-server"'
                    sh 'ssh ec2-user@15.152.41.111 "sudo kubectl rollout restart deployment/mysql-database"'
                }
            }
        }
    }
}
