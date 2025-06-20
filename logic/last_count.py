import os
from flask import jsonify

def read_last_response_counts():
    # ใช้ path แบบ relative จากตำแหน่งไฟล์ปัจจุบันไปยัง static/
    folder_path = os.path.join(os.path.dirname(__file__), "static")

    filenames = {
        "last_response_count_ตอบกลับลูกสูบ.txt": "ปั๊มลมลูกสูบ",
        "last_response_count_ตอบกลับไร้น้ำมัน.txt": "ปั๊มลมไร้น้ำมัน",
        "last_response_count_ตอบกลับโรตารี่.txt": "ปั๊มลมโรตารี่"
    }

    results = {}
    for filename, display_name in filenames.items():
        full_path = os.path.join(folder_path, filename)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                results[display_name] = f.read().strip()
        else:
            results[display_name] = "ไม่พบไฟล์"
    return results
