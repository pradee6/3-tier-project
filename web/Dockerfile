# Use the official Apache HTTP server image
FROM httpd:latest

# Set the working directory inside the container
WORKDIR /usr/local/apache2/htdocs/

# Copy the entire contents of the 'web' folder to Apache's document root inside the container
COPY ./web/ /usr/local/apache2/htdocs/

# Copy the custom Apache configuration file
COPY ./000-default.conf /usr/local/apache2/conf/extra/

# Enable the custom Apache configuration by including it in Apache's main config file
RUN echo "Include conf/extra/000-default.conf" >> /usr/local/apache2/conf/httpd.conf

# Expose port 80 to be accessible from outside the container
EXPOSE 80
