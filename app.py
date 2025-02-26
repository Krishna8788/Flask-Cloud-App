import os
import json
from flask import Flask, request, redirect, url_for, render_template, jsonify
from google.cloud import storage
import google.generativeai as google_ai
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io

app = Flask(__name__)

GCS_BUCKET_NAME = 'my_flask_bucket_for_project'
storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

google_ai.configure(api_key='xxxxxxxxxxxxxxxxxxxxxxxx')
model = google_ai.GenerativeModel('gemini-1.5-flash') 

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def call_google_gemini_ai(prompt, image_bytes):
    try:
        response = model.generate_content([prompt,image_bytes])
        return response.text
    
    except Exception as e:
        print(f"Error calling Google Generative AI: {str(e)[:100]}")
        return None

def clean_and_parse_json(text):
    """Cleans and parses JSON responses from the AI."""
    if not text:
        print("Empty AI response.")
        return None

    text = text.strip("```json").strip("```")
    
    try:
        json_start = text.find('{')
        json_end = text.rfind('}') + 1

        if json_start == -1 or json_end == -1:
            print("No JSON found in AI response.")
            return None

        json_text = text[json_start:json_end]
        return json.loads(json_text)

    except json.JSONDecodeError as error:
        print(f"Error parsing JSON: {error}")
        return None

@app.route('/')
def index():
    blobs = bucket.list_blobs()
    
    images_with_metadata = []
    
    for blob in blobs:
        if blob.name.endswith('.json'):
            continue  # Skip JSON files when listing images
        
        image_url = blob.public_url  # This will only work if public access is enabled
        
        # Fetch associated metadata
        json_blob_name = f"{os.path.splitext(blob.name)[0]}.json"
        json_blob = bucket.blob(json_blob_name)
        
        description = "No description available"
        if json_blob.exists():
            json_data = json_blob.download_as_text()
            try:
                metadata = json.loads(json_data)
                description = metadata.get("description", "No description available")
            except json.JSONDecodeError:
                pass
        
        images_with_metadata.append({"url": image_url, "description": description})

    return render_template('index.html', images=images_with_metadata)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(image.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(image.filename)
    blob = bucket.blob(filename)
    blob.upload_from_file(image, content_type=image.content_type)

    image.seek(0)
    image_data = image.read()
    image.seek(0)

    pil_image = Image.open(io.BytesIO(image_data))
    prompt = """
    Analyze the uploaded image and respond in the following JSON format:
    {
        "description": "A concise description of the image",
        "caption": "A short caption for the image"
    }
    """

    ai_response = call_google_gemini_ai(prompt, pil_image)

    if not ai_response:
        return jsonify({"error": "AI did not return a response"}), 500

    parsed_response = clean_and_parse_json(ai_response)

    if not parsed_response:
        return jsonify({"error": "Failed to parse AI response"}), 500

    metadata = {
        "description": parsed_response.get("description", "No description available"),
        "caption": parsed_response.get("caption", "No caption available")
    }

    json_blob = bucket.blob(f"{os.path.splitext(filename)[0]}.json")
    json_blob.upload_from_string(json.dumps(metadata), content_type='application/json')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
