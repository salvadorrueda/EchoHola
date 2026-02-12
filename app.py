import base64
import os
import uuid
from flask import Flask, render_template, request, jsonify
from recognize import recognize_face, greet

app = Flask(__name__)

# Ensure there's a temp folder for uploads if needed, 
# though we might just save transiently.
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    image_data = data['image']
    
    # Remove the metadata header (e.g., "data:image/jpeg;base64,")
    if ',' in image_data:
        header, encoded = image_data.split(',', 1)
    else:
        encoded = image_data

    try:
        image_bytes = base64.b64decode(encoded)
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        # Call the existing recognition logic
        identity = recognize_face(filepath)
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)
            
        if identity:
            greet(identity)
            return jsonify({'status': 'success', 'identity': identity})
        else:
            # If identity is None, it means verify failed/error, or returning None
            # recognize.py returns "Unknown" explicitly if nobody matches, 
            # but returns None on error (like file not found).
            # Let's handle it gracefully.
            return jsonify({'status': 'success', 'identity': 'Unknown'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    images = data.get('images') # List of base64 strings

    if not name or not images or len(images) == 0:
        return jsonify({'error': 'Missing name or images'}), 400

    # Sanitize name (basic)
    safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).strip()
    if not safe_name:
        return jsonify({'error': 'Invalid name'}), 400

    user_dir = os.path.join('db', safe_name)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    try:
        for i, img_data in enumerate(images):
            if ',' in img_data:
                header, encoded = img_data.split(',', 1)
            else:
                encoded = img_data
            
            image_bytes = base64.b64decode(encoded)
            filename = f"capture_{i+1}.jpg"
            with open(os.path.join(user_dir, filename), "wb") as f:
                f.write(image_bytes)

        # Clear DeepFace pickle files to ensure new user is indexed
        for file in os.listdir('db'):
            if file.endswith('.pkl'):
                os.remove(os.path.join('db', file))
        
        return jsonify({'status': 'success', 'message': f'User {safe_name} registered successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Run EchoHola App")
    parser.add_argument('--https', action='store_true', help="Run with HTTPS (self-signed)")
    args = parser.parse_args()

    run_config = {
        'debug': True,
        'host': '0.0.0.0',
        'port': 5000
    }

    if args.https:
        print("Starting server with HTTPS (ad-hoc SSL context)...")
        run_config['ssl_context'] = 'adhoc'

    app.run(**run_config)
