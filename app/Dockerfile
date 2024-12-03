# Use the official Amazon Linux 2 image as the base image
FROM amazonlinux:2

# Install necessary dependencies
RUN yum update -y && \
    yum install -y python3 python3-pip wget dnf && \
    # Install MySQL 5.7 from Amazon Linux 2 repository
    yum install -y mysql mysql-server && \
    # Clean up cache to reduce image size
    yum clean all

# Install Python dependencies
RUN pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python

# Copy the contents of the app folder into the /app directory in the container
COPY ./app /app

# Set the working directory
WORKDIR /app

# Expose the port that the Flask app will run on
EXPOSE 5000

# Start MySQL server and Flask app in the same container
CMD service mysqld start && \
    mysql -e "CREATE DATABASE IF NOT EXISTS tcs;" && \
    mysql -e "GRANT ALL PRIVILEGES ON tcs.* TO 'root'@'%' IDENTIFIED BY 'rootpassword';" && \
    mysql -e "FLUSH PRIVILEGES;" && \
    python3 app.py
