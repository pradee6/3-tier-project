# Use the official Apache HTTP server image
FROM httpd:latest

# Set the working directory inside the container
WORKDIR /usr/local/apache2/htdocs/

# Copy the entire contents of the 'web' folder to Apache's document root inside the container
COPY ./web/ /usr/local/apache2/htdocs/

# Expose port 80 to be accessible from outside the container
EXPOSE 80

# No need to start Apache manually since it runs by default in the official httpd image
