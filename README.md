Stages Breakdown
1. Checkout Code
Pulls the code from the GitHub repository using credentials and confirms the files are present.
2. SonarQube Analysis
Analyzes the code for bugs, vulnerabilities, and code smells using SonarQube and uploads the results to the SonarQube server.
3. Docker Compose Build
Builds Docker images for the application components (e.g., web server, app server, database) as defined in docker-compose.yml.
4. Trivy Scan
Scans Docker images for vulnerabilities to ensure they are secure before deploying.
5. Tag and Push Images
Tags Docker images with a version (e.g., latest) and pushes them to a container registry (e.g., Docker Hub).
6. Docker Compose Up
Starts the application locally using Docker Compose, ensuring all services are up and running.
7. Kubernetes Login
Copies the Kubernetes deployment file (k8s-deployment.yaml) to the Kubernetes cluster (an EC2 instance).
8. Kubernetes Deployment
Applies the Kubernetes deployment configuration on the cluster to deploy the application.
Restarts the Kubernetes pods for the web server, app server, and database to ensure the latest configurations and images are used.
