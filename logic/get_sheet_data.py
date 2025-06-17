#แก้ google sheet ด้วย
from flask import jsonify
from utils.gsheet import client
from datetime import datetime
import pytz
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

        tz = pytz.timezone("Asia/Bangkok")
        now = datetime.now(tz)
        year = now.year - 543 if now.year > 2500 else now.year
        d, m = now.day, now.month

        today_formats = [
            f"{d}/{m}/{year}",
            f"{d:02d}/{m}/{year}",
            f"{d}/{m:02d}/{year}",
            f"{d:02d}/{m:02d}/{year}"
        ]
        '''
        date_cols = ["O", "S", "W", "AA"]
        date_col_indexes = [colname_to_index(c) for c in date_cols]
        description_col = colname_to_index("B")'''
        date_col_indexes = [colname_to_index("D")]  # วันที่
        description_col = colname_to_index("I")     # Description (ใหม่)
        qa_col = colname_to_index("L")              # จำนวนสุ่ม QA:
        done_col = colname_to_index("M")            # จำนวนที่ทำแล้ว

        matched_data = []

        for row_idx, row in enumerate(rows, start=2):
            for col_idx in date_col_indexes:
                if len(row) > col_idx:
                    cell_value = str(row[col_idx]).strip()
                    if any(fmt in cell_value for fmt in today_formats):
                        description = row[description_col] if len(row) > description_col else "-"
                        prev_col_idx = col_idx - 1
                        next_col_idx = col_idx + 1

                        value_prev_column = row[prev_col_idx] if prev_col_idx >= 0 and len(row) > prev_col_idx else "-"
                        value_next_column = row[next_col_idx] if next_col_idx < len(row) else "-"
                        '''
                        matched_data.append({
                            "description": description,
                            "date_value": cell_value,
                            "value_prev_column": value_prev_column,  # จำนวนสุ่ม QA:
                            "value_next_column": value_next_column    # คอลัมน์ถัดจากวันที่
                        })'''
                        matched_data.append({
                            "description": row[description_col] if len(row) > description_col else "-",
                            "date_value": cell_value,
                            "value_prev_column": row[qa_col] if len(row) > qa_col else "-",
                            "value_next_column": row[done_col] if len(row) > done_col else "-"
                        })
                        break

        return jsonify({"status": "success", "data": matched_data})

    except Exception as e:
        logging.error("เกิดข้อผิดพลาด:", exc_info=True)
        return jsonify({"status": "error", "message": str(e)})
