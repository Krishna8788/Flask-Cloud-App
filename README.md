# Flask Image Upload Application

## Project Overview
This project is a Flask-based web application that allows users to upload images, which are then stored in Google Cloud Storage. The application is containerized using Docker and deployed on Google Cloud Run to provide scalability, reliability, and cost-effectiveness. The project demonstrates the integration of Flask with Google Cloud services for serverless and efficient image management.

## Features
- User-friendly web interface for image uploads
- Secure storage using Google Cloud Storage (GCS)
- Public URLs for uploaded images
- Scalable and serverless deployment using Google Cloud Run
- Containerized environment for easy deployment and management

## Architecture

The project follows a cloud-based microservices architecture with the following components:

- **Frontend:**
  - HTML form with Bootstrap for responsive design
  - Client-side validation for image uploads

- **Backend:**
  - Flask web framework to handle HTTP requests
  - Google Cloud Storage integration for storing uploaded images
  - Error handling and logging for application monitoring

- **Deployment:**
  - Docker containerization for environment consistency
  - Google Cloud Run for serverless deployment with autoscaling
  - Google Container Registry for image storage

## Technologies Used
- **Backend:** Flask (Python)
- **Cloud Services:**
  - Google Cloud Storage (GCS)
  - Google Cloud Run
  - Google Container Registry (GCR)
- **Containerization:** Docker
- **Frontend:** HTML, CSS, Bootstrap
- **Version Control:** Git and GitHub

## Prerequisites
Before running the project, ensure you have the following installed:

- Python 3.9+
- Google Cloud SDK
- Docker
- Git

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Google Cloud Credentials
1. Create a Google Cloud Storage bucket.
2. Download the service account JSON key and place it in the project root.
3. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path-to-your-service-account-key.json"
   ```

### 4. Run the Application Locally
```bash
python cloud_image_app.py
```

Access the app at `http://127.0.0.1:5000` and test the upload functionality.

## Dockerization

### 1. Build Docker Image
```bash
docker build -t flask-image-app .
```

### 2. Run Docker Container
```bash
docker run -p 8080:8080 flask-image-app
```

## Deploying to Google Cloud Run

### 1. Authenticate Google Cloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Push Docker Image to Google Container Registry
```bash
docker tag flask-image-app gcr.io/YOUR_PROJECT_ID/flask-image-app
docker push gcr.io/YOUR_PROJECT_ID/flask-image-app
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy flask-image-app \
    --image gcr.io/YOUR_PROJECT_ID/flask-image-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### 4. Get the Deployed App URL
```bash
gcloud run services describe flask-image-app --format 'value(status.url)'
```

## Application Usage
1. Open the deployed URL in your browser.
2. Upload images using the provided form.
3. View uploaded images with their public URLs.

## Challenges Faced
- Managing cloud storage permissions
- Handling cold starts in serverless deployment
- Ensuring secure storage of credentials

## Future Improvements
- Implementing user authentication
- Adding metadata storage with a database
- Enhancing UI with additional functionalities
- Automating deployment using CI/CD pipelines

## Security Considerations
- Restricting public access to sensitive data
- Using environment variables to manage credentials
- Enabling HTTPS for secure communication

## Contributing
Contributions are welcome! Feel free to submit pull requests with improvements or bug fixes.

