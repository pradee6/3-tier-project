# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
# This improves build time by caching dependencies
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Now, copy the rest of the application files into the container
COPY . /app/

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
