#แก้ google sheet ด้วย
import re
import pytz
import os
from datetime import datetime
from flask import jsonify, request
from collections import defaultdict
from utils.gsheet import client

def normalize_model(text):
    return re.sub(r'[\s\-\(\)]', '', text.upper())

def colname_to_index(colname):
    colname = colname.upper()
    index = 0
    for char in colname:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1

def check_and_deduct_logic():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1bief199t8kf8vV9NoAUl_sakTTBTne5tKbXW8z65TcQ/edit"
        workbook = client.open_by_url(sheet_url)
        main_sheet = workbook.worksheet("2025")
        response_sheets = ["ตอบกลับลูกสูบ", "ตอบกลับไร้น้ำมัน", "ตอบกลับโรตารี่"]

        # ดึง model จาก request
        req_data = request.get_json()
        target_models = req_data.get("models")
        if target_models:
            if isinstance(target_models, str):
                target_models = [target_models]
            target_model_clean_set = set(normalize_model(m.strip().upper()) for m in target_models)
        else:
            target_model_clean_set = None  # หมายถึงไม่กรองด้วย model

        tz = pytz.timezone("Asia/Bangkok")
        now = datetime.now(tz)
        year = now.year - 543 if now.year > 2500 else now.year
        d, m = now.day, now.month
        today_formats = [
            f"{d}/{m}/{year}", f"{d:02d}/{m}/{year}",
            f"{d}/{m:02d}/{year}", f"{d:02d}/{m:02d}/{year}"
        ]

        headers_map = {}
        new_model_counts = defaultdict(int)

        # วนลูปแต่ละชีต
        for sheet_name in response_sheets:
            sheet = workbook.worksheet(sheet_name)
            values = sheet.get_all_values()
            if not values or len(values) <= 1:
                continue

            headers = values[0]
            rows = values[1:]
            model_index = next((i for i, h in enumerate(headers) if "model" in h.lower()), 6)
            date_index = next((i for i, h in enumerate(headers) if "วันที่ตรวจ" in h), 1)

            # ไฟล์นับแยกตามชีต
            counter_file = f"last_response_count_{sheet_name}.txt"
            last_count = 0
            if os.path.exists(counter_file):
                with open(counter_file, "r") as f:
                    try:
                        last_count = int(f.read().strip())
                    except:
                        pass

            current_count = len(rows)
            new_rows = rows[last_count:]

            for row in new_rows:
                if len(row) > max(model_index, date_index):
                    model_raw = row[model_index].strip().upper()
                    model_clean = normalize_model(model_raw)
                    date_val = row[date_index].strip()

                    if (target_model_clean_set is None or model_clean in target_model_clean_set) and date_val in today_formats:
                        new_model_counts[model_clean] += 1

            # บันทึก count ใหม่ไว้
            with open(counter_file, "w") as f:
                f.write(str(current_count))

        # อ่านข้อมูลหลัก
        main_data = main_sheet.get_all_values()
        desc_col_index = colname_to_index("B")
        date_cols = ["O", "S", "W", "AA"]
        date_indexes = [colname_to_index(c) for c in date_cols]

        summary = []

        for model_key, count in new_model_counts.items():
            matched_row_index = None
            for i, row in enumerate(main_data[1:], start=2):
                if len(row) > desc_col_index:
                    desc_clean = normalize_model(row[desc_col_index].strip())
                    if model_key in desc_clean:
                        matched_row_index = i
                        break

            if not matched_row_index:
                summary.append(f"{model_key}: ❌ ไม่พบ MODEL ในชีตหลัก")
                continue

            matched_row = main_data[matched_row_index - 1]
            matched_date_col = None
            for col_idx in date_indexes:
                if len(matched_row) > col_idx:
                    val = matched_row[col_idx].strip()
                    if val in today_formats:
                        matched_date_col = col_idx
                        break

            if matched_date_col is None:
                summary.append(f"{model_key}: ❌ ไม่พบวันที่ใน O/S/W/AA")
                continue

            write_col = matched_date_col + 1
            old_val = matched_row[write_col] if len(matched_row) > write_col else "0"
            try:
                old_int = int(old_val) if old_val.strip().isdigit() else 0
                new_val = old_int + count
                main_sheet.update_cell(matched_row_index, write_col + 1, str(new_val))
                summary.append(f"{model_key}: ✅ บวก +{count} → {new_val}")
            except Exception as e:
                summary.append(f"{model_key}: ❌ Error เขียนค่าลงชีต - {str(e)}")

        if not summary:
            summary.append("⛔ ไม่มีข้อมูลใหม่ที่ตรงกับวันนี้")

        return jsonify({"status": "success", "message": "\n".join(summary)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
