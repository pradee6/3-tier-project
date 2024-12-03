# Use Amazon Linux 2 as the base image
FROM amazonlinux:2

# Install system dependencies and Python 3
RUN yum update -y && \
    yum install -y python3 python3-pip && \
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

# Expose the Flask application port
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Start the Flask application
CMD ["python3", "app.py"]
