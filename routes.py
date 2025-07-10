from flask import render_template, request, jsonify
from logic.submit import submit_qr_logic
from logic.check_deduct import check_and_deduct_logic
from logic.get_sheet_data_column_N import get_sheet_data
from logic.ocr import ocr_from_image
from logic.chatAI import chat_ai_logic
from logic.last_count import read_last_response_counts
from flask import send_from_directory, abort

def register_routes(app):
    @app.route('/')
    def index():
        return render_template("index7.html")

    @app.route('/submit_qr', methods=['POST']) # ไว้ใช้เรียกคำสั่งไป index.html
    def submit_qr():
        return submit_qr_logic(request)

    @app.route('/get_sheet_data')
    def get_sheet_data_route():
        return get_sheet_data()

    @app.route('/update_count_with_txt', methods=['POST']) # ไว้ใช้เรียกคำสั่งไป index.html
    def check_deduct_route():
        return check_and_deduct_logic()
    
    @app.route('/show_last_counts')
    def show_last_counts():
        return jsonify(read_last_response_counts())
    
    @app.route('/chat_ai', methods=['POST']) # ไว้ใช้เรียกคำสั่งไป index.html
    def chat_ai():
        return chat_ai_logic(request)
    
    @app.route('/static/<path:filename>')
    def serve_static_txt(filename):
        if filename.endswith(".txt"):
            return send_from_directory('static', filename)
        else:
            abort(404)
