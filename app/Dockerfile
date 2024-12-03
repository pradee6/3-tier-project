# Use Amazon Linux 2 as the base image
FROM amazonlinux:2

# Install system dependencies, Python 3, and MySQL
RUN yum update -y && \
    yum install -y python3 python3-pip mysql-server && \
    yum clean all

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Set the working directory for the application
WORKDIR /app

# Copy the application dependencies file (requirements.txt)
COPY app/requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files into the container
COPY app/ /app/

# Expose ports for Flask and MySQL
EXPOSE 5000 3306

# Define environment variables for Flask and MySQL
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=pradeep
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

# Add a script to initialize MySQL and Flask
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start MySQL and Flask
CMD ["/start.sh"]
