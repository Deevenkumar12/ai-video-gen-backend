from flask import Flask, request, jsonify
import replicate
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

os.environ["REPLICATE_API_TOKEN"] = "r8_3KygRMXGurnaNVvsIsuePjSj698eWW048zce6"

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
