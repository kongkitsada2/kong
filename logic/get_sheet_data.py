from flask import jsonify
from utils.gsheet import client
import logging

logging.basicConfig(level=logging.INFO)

def colname_to_index(colname):
    colname = colname.upper()
    index = 0
    for char in colname:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1

def get_sheet_data():
    try:
        sheet = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/1bief199t8kf8vV9NoAUl_sakTTBTne5tKbXW8z65TcQ/edit"
        ).worksheet("รายงานผลQCรายวัน")

        values = sheet.get_all_values()
        if not values or len(values) < 2:
            return jsonify({"status": "success", "data": []})

        headers = values[0]
        rows = values[1:]

        # ✅ ตั้งค่าคอลัมน์ที่ต้องใช้
        description_col = colname_to_index("I")  # Description
        qa_col = colname_to_index("L")           # จำนวนสุ่ม QA:
        done_col = colname_to_index("M")         # จำนวนที่ทำแล้ว
        remain_col = colname_to_index("N")       # คงเหลือ

        matched_data = []

        for row in rows:
            try:
                remain_value = int(str(row[remain_col]).strip()) if len(row) > remain_col else 0
            except:
                remain_value = 0

            if remain_value > 0:
                matched_data.append({
                    "description": row[description_col] if len(row) > description_col else "-",
                    "date_value": str(remain_value),
                    "value_prev_column": row[qa_col] if len(row) > qa_col else "-",
                    "value_next_column": row[done_col] if len(row) > done_col else "-"
                })

        return jsonify({"status": "success", "data": matched_data})

    except Exception as e:
        logging.error("เกิดข้อผิดพลาด:", exc_info=True)
        return jsonify({"status": "error", "message": str(e)})
