# Dockerfile

# Use official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the app files to the container
COPY app.py /app
COPY templates /app/templates

# Install dependencies
RUN pip install flask pymongo requests

# Expose port 5000 for Flask app
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]

