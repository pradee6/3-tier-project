# Use the Amazon Linux 2023 base image
FROM amazonlinux:2023

# Update the system and install necessary tools
RUN yum update -y && \
    yum install -y wget dnf python3 python3-pip

# Install MySQL 8.0 Community Edition
RUN wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm && \
    dnf install -y mysql80-community-release-el9-1.noarch.rpm && \
    rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2023 && \
    dnf install -y mysql-community-client mysql-community-server

# Start MySQL service (in Docker, this won't run as a background service, so we won't actually need it running)
RUN systemctl enable mysqld

# Install Python dependencies
RUN pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python SQLAlchemy

# Set the working directory for the application
WORKDIR /app

# Copy the Flask app code into the container
COPY . /app

# Expose the port Flask will run on
EXPOSE 5000

# Command to start your Flask app
CMD ["python3", "app.py"]
