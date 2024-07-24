from flask import Flask, request, jsonify
import base64
import io
from PIL import Image

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data.get('image')

    # Extract base64 data
    header, encoded = image_data.split(',', 1)
    decoded = base64.b64decode(encoded)
    
    # Load image with PIL (Python Imaging Library)
    image = Image.open(io.BytesIO(decoded))
    
    # You can now process the image (save, analyze, etc.)
    image.save('uploaded_image.png')
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
