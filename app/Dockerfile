# Use Amazon Linux 2023 as the base image
FROM amazonlinux:2023

# Set environment variables to reduce warnings and make installations smoother
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install dependencies for MySQL and Python
RUN yum update -y && \
    yum install -y python3 python3-pip wget dnf && \
    yum install -y mysql80-community-release-el9-1.noarch.rpm && \
    yum install -y mysql-community-client mysql-community-server && \
    pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python

# Set environment variables for MySQL (ensure to configure these based on your app's needs)
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=app_db

# Expose the ports MySQL and Flask will run on
EXPOSE 3306 5000

# Start MySQL and Flask application
CMD /usr/bin/mysqld_safe & python3 app.py
