# Use the official MySQL image from Docker Hub as the base image
FROM mysql:latest

# Set environment variables to configure the MySQL database
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=tcs
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=userpassword

# Optional: If you have any initialization SQL scripts, copy them into the container
# These scripts will be automatically executed when the container is first created.
# COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose the MySQL default port (3306)
EXPOSE 3306
