from flask import Flask, render_template, request, send_file
import requests
import os
from dotenv import load_dotenv
import base64
from io import BytesIO

load_dotenv()

app = Flask(__name__)

# Configure your API key
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        
        # Call Stable Diffusion API
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }
        
        body = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }
        
        try:
            response = requests.post(url, headers=headers, json=body)
            if response.status_code == 200:
                # Get base64 image from response
                image_data = response.json()['artifacts'][0]['base64']
                image = BytesIO(base64.b64decode(image_data))
                return send_file(image, mimetype='image/png')
            else:
                return f"Error: {response.status_code}", 400
        except Exception as e:
            return str(e), 500
    
    return render_template('index.html')

# Create templates/index.html
if not os.path.exists('templates'):
    os.makedirs('templates')
    
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Text to Image Generator</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { display: flex; flex-direction: column; gap: 20px; }
        input[type="text"] { padding: 10px; width: 100%; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        #result { margin-top: 20px; }
        img { max-width: 100%; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text to Image Generator</h1>
        <form method="POST">
            <input type="text" name="prompt" placeholder="Enter your image description..." required>
            <button type="submit">Generate Image</button>
        </form>
        <div id="result">
            {% if image_path %}
            <img src="{{ image_path }}" alt="Generated image">
            {% endif %}
        </div>
    </div>
</body>
</html>
""")

if __name__ == '__main__':
    app.run(debug=True)