'''project/
│
├── app.py                       ← ✅ รันจากไฟล์นี้
├── routes.py                   ← เก็บเส้นทาง (routes)
│
├── logic/                      ← ฟังก์ชันหลักของระบบ
│   ├── submit.py
│   ├── check_deduct.py
│   └── get_sheet_data.py
│
└── utils/                      ← ยูทิลิตี้ เช่น Google Sheet API
    └── gsheet.py'''


from flask import Flask, send_from_directory, abort
from routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.route('/<filename>')
def serve_txt_from_root(filename):
    if filename.endswith(".txt"):
        return send_from_directory('.', filename)
    else:
        abort(404)  # ป้องกันการเข้าถึงไฟล์อื่น

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('192.168.1.120.pem', '192.168.1.120-key.pem'))
'''
