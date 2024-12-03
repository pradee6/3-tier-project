# Use Amazon Linux 2023 as the base image
FROM amazonlinux:2023

# Set environment variables to reduce warnings and make installations smoother
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python, pip, and other dependencies
RUN yum update -y && \
    yum install -y python3 python3-pip wget dnf

# Install MySQL client (if your Flask app needs to connect to MySQL)
RUN yum install -y mysql-community-client

# Install Python packages required for the Flask app
RUN pip3 install Flask Flask-SQLAlchemy Flask-Mail Flask-CORS Flask-Session mysql-connector-python

# Expose the Flask application port (5000 for Flask)
EXPOSE 5000

# Start the Flask application
CMD ["python3", "app.py"]  # Assuming your main Flask app file is named app.py
