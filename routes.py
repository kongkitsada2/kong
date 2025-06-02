from flask import render_template, request, jsonify
from logic.submit import submit_qr_logic
from logic.check_deduct import check_and_deduct_logic
from logic.get_sheet_data import get_sheet_data
from logic.ocr import ocr_from_image
from logic.chatAI import chat_ai_logic

def register_routes(app):
    @app.route('/')
    def index():
        return render_template("index6.html")

    @app.route('/submit_qr', methods=['POST'])
    def submit_qr():
        return submit_qr_logic(request)

    @app.route('/get_sheet_data')
    def get_sheet_data_route():
        return get_sheet_data()

    @app.route('/check_and_deduct_new_form_data', methods=['POST'])
    def check_and_deduct():
        return check_and_deduct_logic()

    @app.route('/upload_image_ocr', methods=['POST'])
    def upload_image_ocr():
        return ocr_from_image(request)
    
    @app.route('/chat_ai', methods=['POST'])
    def chat_ai():
        return chat_ai_logic(request)