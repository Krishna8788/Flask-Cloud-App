from flask import Flask, request, render_template
from google.cloud import storage
import os

app = Flask(__name__)

# Configure Google Cloud Storage
GCS_BUCKET_NAME = 'my_flask_bucket_for_project'
GCS_CREDENTIALS_PATH = './flask-storage-access-a0832d4a7f1b.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCS_CREDENTIALS_PATH

storage_client = storage.Client()
bucket = storage_client.get_bucket(GCS_BUCKET_NAME)

@app.route('/')
def index():
    blobs = bucket.list_blobs()
    image_urls = [blob.public_url for blob in blobs]
    return render_template('index.html', images=image_urls)

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    blob = bucket.blob(image.filename)
    blob.upload_from_file(image)
    blob.make_public()
    return 'Image uploaded successfully: <a href="/">View Images</a>'

if __name__ == '__main__':
    app.run(debug=True)

