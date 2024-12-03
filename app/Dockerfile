# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY app/requirements.txt /app/

# Install dependencies
RUN pip install -r /app/requirements.txt

# Now, copy the rest of the application files into the container
COPY app/ /app/

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# MySQL configuration
# MySQL container name
ENV MYSQL_HOST=db

# MySQL username
ENV MYSQL_USER=user

# MySQL password
ENV MYSQL_PASSWORD=password

# MySQL database name
ENV MYSQL_DATABASE=pradeep

# Run the Flask application using python directly
CMD ["python", "app.py"]
