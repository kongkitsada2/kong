from flask import render_template, request, jsonify
from logic.submit import submit_qr_logic
from logic.check_deduct import check_and_deduct_logic
from logic.get_sheet_data_column_N import get_sheet_data
from logic.chatAI import chat_ai_logic
from logic.last_count import read_last_response_counts

def register_routes(app):
    @app.route('/')
    def index():
        return render_template("index7.html")

    @app.route('/submit_qr', methods=['POST'])
    def submit_qr():
        return submit_qr_logic(request)

    @app.route('/get_sheet_data')
    def get_sheet_data_route():
        return get_sheet_data()

    @app.route('/check_and_deduct_new_form_data', methods=['POST'])
    def check_and_deduct():
        return check_and_deduct_logic()
    
    @app.route('/chat_ai', methods=['POST'])
    def chat_ai():
        return chat_ai_logic(request)
        
    @app.route('/show_last_counts')
    def show_last_counts():
        return jsonify(read_last_response_counts())
