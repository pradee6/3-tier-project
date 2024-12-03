# Use Amazon Linux 2023 as the base image
FROM amazonlinux:2023

# Set environment variables to reduce warnings and make installations smoother
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python, pip, and other dependencies
RUN yum update -y && \
    yum install -y python3 python3-pip wget dnf

# Install MySQL 8.0 community release and client
RUN wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm && \
    rpm -ivh mysql80-community-release-el9-1.noarch.rpm && \
    yum install -y mysql-community-client mysql-community-server

# Install Python packages required for the Flask app
RUN pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python

# Start MySQL service and enable it
RUN systemctl enable mysqld

# Expose the port MySQL will run on
EXPOSE 3306

# Expose the Flask application port (e.g., 5000 for Flask)
EXPOSE 5000

# Start MySQL and the Flask application
CMD service mysqld start && \
    python3 app.py  # Assuming your main Flask app file is named app.py
