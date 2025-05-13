from flask import Flask, request, jsonify
import replicate
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Use the Replicate token from env variables
os.environ["REPLICATE_API_TOKEN"] = os.getenv("r8_BKfeyEOstB8Lzb0JT7LNWSIfaS5FAPL3mJHKw")

@app.route("/generate", methods=["POST"])
def generate():
    image = request.files['image']
    prompt = request.form['prompt']
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    output = replicate.run(
        "ali-vilab/modelscope:8f26c504e07c65f5edfb9b6e8c7e0659d116b27dc5f5a269eb2332f2023f543e",
        input={"image": open(filepath, "rb"), "prompt": prompt}
    )
    
    return jsonify({"video_url": output})

# ✅ Required for Render to bind port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
