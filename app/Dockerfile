# Use Amazon Linux 2023 as the base image
FROM amazonlinux:2023

# Set environment variables to reduce warnings and make installations smoother
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python, pip, and other dependencies
RUN yum update -y && \
    yum install -y python3 python3-pip wget dnf mysql-community-client mysql-community-server

# Install Python packages required for the Flask app
RUN pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python

# Install MySQL community release and client
RUN wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm && \
    rpm -ivh mysql80-community-release-el9-1.noarch.rpm && \
    dnf install -y mysql80-community-release-el9-1.noarch.rpm

# Install MySQL server and start it
RUN dnf install -y mysql-community-server && \
    systemctl enable mysqld

# Copy your Flask application code into the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app

# Expose the port MySQL will run on
EXPOSE 3306

# Expose the Flask application port (e.g., 5000 for Flask)
EXPOSE 5000

# Start MySQL and the Flask application
CMD service mysqld start && \
    python3 app.py  # Assuming your main Flask app file is named app.py
