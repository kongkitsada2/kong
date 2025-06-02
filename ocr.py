from flask import jsonify
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_from_image(request):
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "ไม่มีไฟล์ภาพ"}), 400

        image = Image.open(request.files['image'].stream).convert("RGB")
        width, height = image.size

        data = pytesseract.image_to_data(image, lang='eng+tha', output_type=pytesseract.Output.DICT)

        results = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 60 and data['text'][i].strip():  # confidence > 60%
                results.append({
                    "text": data['text'][i],
                    "left": data['left'][i],
                    "top": data['top'][i],
                    "width": data['width'][i],
                    "height": data['height'][i]
                })

        return jsonify({"status": "success", "results": results, "image_size": [width, height]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
