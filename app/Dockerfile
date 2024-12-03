# Use the official Amazon Linux 2023 image as the base image
FROM amazonlinux:2023

# Install necessary dependencies
RUN yum update -y && \
    yum install -y python3 python3-pip wget dnf && \
    # Install the MySQL 8.0 repository
    wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm && \
    yum localinstall -y mysql80-community-release-el9-1.noarch.rpm && \
    # Install MySQL client and server
    yum install -y mysql-community-client mysql-community-server && \
    # Clean up the rpm file
    rm -f mysql80-community-release-el9-1.noarch.rpm

# Install Python dependencies
RUN pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python

# Copy the contents of the app folder into the /app directory in the container
COPY ./app /app

# Set the working directory
WORKDIR /app

# Expose the port that the Flask app will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "app.py"]
