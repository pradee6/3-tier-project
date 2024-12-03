# Use Python base image
FROM python:3.9-slim

# Install MySQL server and client
RUN apt-get update && \
    apt-get install -y mysql-server mysql-client libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Install required Python dependencies (Flask, SQLAlchemy, MySQL connector)
RUN pip install --no-cache-dir flask flask-mysqldb mysql-connector-python flask-sqlalchemy

# Set working directory
WORKDIR /app

# Copy the Flask application files to the container
COPY . /app

# Expose the port that the app will run on
EXPOSE 5000

# Set the environment variables for MySQL user and password
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_USER=flaskuser
ENV MYSQL_PASSWORD=flaskpassword
ENV MYSQL_DATABASE=tcs

# Initialize MySQL database and start the Flask app
CMD service mysql start && \
    mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;" && \
    mysql -e "CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';" && \
    mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%';" && \
    mysql -e "FLUSH PRIVILEGES;" && \
    python3 /app/app.py
