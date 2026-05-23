
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import TrOCRProcessor
from transformers import VisionEncoderDecoderModel
from PIL import Image
import cv2
import os

app = Flask(__name__)
CORS(app)

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

UPLOAD_FOLDER = "uploads"

@app.route('/upload', methods=['POST'])
def upload():

    if 'image' not in request.files:
        return jsonify({
            "error": "No image uploaded"
        })

    image_file = request.files['image']

    image_path = os.path.join(
        UPLOAD_FOLDER,
        image_file.filename
    )

    image_file.save(image_path)

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    cv2.imwrite(image_path, thresh)

    image = Image.open(image_path).convert("RGB")

    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values

    generated_ids = model.generate(pixel_values)

    generated_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return jsonify({
        "text": generated_text
    })

if __name__ == '__main__':
    app.run(debug=True)
