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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
