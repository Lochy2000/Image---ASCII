from flask import Flask, render_template, request, send_file, jsonify
import requests
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
import uuid
from datetime import datetime

load_dotenv()
app = Flask(__name__)

STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
UPLOAD_FOLDER = 'generated_images'

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]  # Remove the data:image/png;base64 prefix
        prompt = data['prompt'][:30]  # Take first 30 chars of prompt for filename
        
        # Create a filename with timestamp and sanitized prompt
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_prompt = "".join(x for x in prompt if x.isalnum() or x in (' ', '-', '_')).strip()
        filename = f"{timestamp}_{safe_prompt}_{str(uuid.uuid4())[:8]}.png"
        
        # Save the image
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(img_path, 'wb') as f:
            f.write(base64.b64decode(image_data))
            
        return jsonify({
            'success': True,
            'message': 'Image saved successfully',
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving image: {str(e)}'
        }), 500

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get all parameters from the form
        data = request.get_json()
        prompt = data['prompt']
        negative_prompt = data.get('negative_prompt', '')
        style_preset = data.get('style_preset', 'none')
        
        # Advanced parameters
        cfg_scale = float(data.get('cfg_scale', 7))
        steps = int(data.get('steps', 30))
        width = int(data.get('width', 1024))
        height = int(data.get('height', 1024))
        samples = int(data.get('samples', 1))
        
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        }
        
        # Construct text prompts with weights
        text_prompts = [{"text": prompt, "weight": 1}]
        if negative_prompt:
            text_prompts.append({"text": negative_prompt, "weight": -1})
        
        body = {
            "text_prompts": text_prompts,
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps,
            "style_preset": style_preset if style_preset != 'none' else None
        }
        # [Previous code remains the same until the response handling]
        try:
            response = requests.post(url, headers=headers, json=body)
            if response.status_code == 200:
                images = []
                for artifact in response.json()['artifacts']:
                    image_data = artifact['base64']
                    images.append(f"data:image/png;base64,{image_data}")
                return jsonify({
                    'images': images,
                    'prompt': prompt  # Send prompt back for filename creation
                })
            else:
                return jsonify({'error': f"API Error: {response.status_code}"}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('index.html')

# Update the HTML template
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Advanced Image Generator</title>
    <style>
                body { font-family: Arial; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .container { display: flex; flex-direction: column; gap: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        textarea, input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
        }
        .advanced-controls {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .controls-toggle {
            background: #007bff;
            color: white;
            padding: 10px;
            border: none;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .generate-btn {
            padding: 15px 30px;
            background: #28a745;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .gallery img {
            width: 100%;
            height: auto;
            border-radius: 5px;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }

        /* Previous styles remain the same */
        .image-container {
            position: relative;
            margin-bottom: 20px;
        }
        .save-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #28a745;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
            cursor: pointer;
            opacity: 0.9;
        }
        .save-btn:hover {
            opacity: 1;
        }
        .save-status {
            position: absolute;
            top: 10px;
            right: 90px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
            display: none;
        }
    </style>
</head>
<body>
       <div class="container">
        <h1>Advanced Image Generator</h1>
        
        <div class="form-group">
            <label for="prompt">Prompt:</label>
            <textarea id="prompt" rows="4" placeholder="Describe what you want to see in detail..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="negative_prompt">Negative Prompt (what to avoid):</label>
            <textarea id="negative_prompt" rows="2" placeholder="Describe what you don't want to see..."></textarea>
        </div>
        
        <button class="controls-toggle" onclick="toggleAdvanced()">Toggle Advanced Controls</button>
        
        <div class="advanced-controls" id="advancedControls" style="display: none;">
            <div class="form-group">
                <label for="style_preset">Style Preset:</label>
                <select id="style_preset">
                    <option value="none">None</option>
                    <option value="3d-model">3D Model</option>
                    <option value="analog-film">Analog Film</option>
                    <option value="anime">Anime</option>
                    <option value="cinematic">Cinematic</option>
                    <option value="comic-book">Comic Book</option>
                    <option value="digital-art">Digital Art</option>
                    <option value="enhance">Enhance</option>
                    <option value="fantasy-art">Fantasy Art</option>
                    <option value="isometric">Isometric</option>
                    <option value="line-art">Line Art</option>
                    <option value="low-poly">Low Poly</option>
                    <option value="modeling-compound">Modeling Compound</option>
                    <option value="neon-punk">Neon Punk</option>
                    <option value="origami">Origami</option>
                    <option value="photographic">Photographic</option>
                    <option value="pixel-art">Pixel Art</option>
                    <option value="tile-texture">Tile Texture</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="cfg_scale">CFG Scale (how closely to follow prompt: 1-20):</label>
                <input type="number" id="cfg_scale" value="7" min="1" max="20">
            </div>
            
            <div class="form-group">
                <label for="steps">Steps (more = higher quality but slower: 10-50):</label>
                <input type="number" id="steps" value="30" min="10" max="50">
            </div>
            
            <div class="form-group">
                <label for="samples">Number of Images:</label>
                <input type="number" id="samples" value="1" min="1" max="4">
            </div>
            
            <div class="form-group">
                <label>Image Size:</label>
                <select id="size">
                    <option value="1024x1024">1024x1024 (Square)</option>
                    <option value="1024x1792">1024x1792 (Portrait)</option>
                    <option value="1792x1024">1792x1024 (Landscape)</option>
                </select>
            </div>
        </div>
        
        <button class="generate-btn" onclick="generateImage()">Generate Image</button>
        
        <div class="loading" id="loading">
            Generating your image... This may take a few moments...
        </div>
            
    <!-- Previous HTML remains the same until the gallery div -->
    <div class="gallery" id="gallery"></div>

    <script>
        let currentPrompt = '';

        function toggleAdvanced() {
            const controls = document.getElementById('advancedControls');
            controls.style.display = controls.style.display === 'none' ? 'block' : 'none';
        }

        async function saveImage(imageData, imageContainer) {
            const saveBtn = imageContainer.querySelector('.save-btn');
            const saveStatus = imageContainer.querySelector('.save-status');
            
            saveBtn.disabled = true;
            saveStatus.textContent = 'Saving...';
            saveStatus.style.display = 'block';
            
            try {
                const response = await fetch('/save-image', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        image: imageData,
                        prompt: currentPrompt
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    saveStatus.textContent = 'Saved!';
                    saveBtn.style.display = 'none';
                    setTimeout(() => {
                        saveStatus.style.display = 'none';
                    }, 2000);
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                saveStatus.textContent = 'Error saving';
                saveBtn.disabled = false;
                setTimeout(() => {
                    saveStatus.style.display = 'none';
                }, 2000);
                console.error('Error:', error);
            }
        }

        function generateImage() {
            const loading = document.getElementById('loading');
            const gallery = document.getElementById('gallery');
            const sizeSelect = document.getElementById('size');
            const [width, height] = sizeSelect.value.split('x').map(Number);
            
            loading.style.display = 'block';
            gallery.innerHTML = '';
            
            currentPrompt = document.getElementById('prompt').value;
            
            const data = {
                prompt: currentPrompt,
                negative_prompt: document.getElementById('negative_prompt').value,
                style_preset: document.getElementById('style_preset').value,
                cfg_scale: document.getElementById('cfg_scale').value,
                steps: document.getElementById('steps').value,
                samples: document.getElementById('samples').value,
                width: width,
                height: height
            };
            
            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    alert(data.error);
                    return;
                }
                data.images.forEach(imageData => {
                    const container = document.createElement('div');
                    container.className = 'image-container';
                    
                    const img = document.createElement('img');
                    img.src = imageData;
                    
                    const saveBtn = document.createElement('button');
                    saveBtn.className = 'save-btn';
                    saveBtn.textContent = 'Save';
                    saveBtn.onclick = () => saveImage(imageData, container);
                    
                    const saveStatus = document.createElement('div');
                    saveStatus.className = 'save-status';
                    
                    container.appendChild(img);
                    container.appendChild(saveBtn);
                    container.appendChild(saveStatus);
                    gallery.appendChild(container);
                });
            })
            .catch(error => {
                loading.style.display = 'none';
                alert('Error: ' + error);
            });
        }
    </script>
</body>
</html>
""")

if __name__ == '__main__':
    app.run(debug=True)