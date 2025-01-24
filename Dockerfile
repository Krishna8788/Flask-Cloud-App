# Use the official Python image as a base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install dependencies
RUN pip install Flask google-cloud-storage gunicorn

# Set environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="./flask-storage-access-a0832d4a7f1b.json"

# Expose port 8080 for running the app in Cloud Run
EXPOSE 8080

# Command to run the application using Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
