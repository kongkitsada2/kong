import re
import os
from flask import jsonify, request
from collections import defaultdict
from utils.gsheet import client

def normalize_model(text):
    return re.sub(r'[\s\-\(\)]', '', text.upper())

def check_and_deduct_logic():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1bief199t8kf8vV9NoAUl_sakTTBTne5tKbXW8z65TcQ/edit"
        workbook = client.open_by_url(sheet_url)
        main_sheet = workbook.worksheet("รายงานผลQCรายวัน")
        response_sheets = ["ตอบกลับลูกสูบ", "ตอบกลับไร้น้ำมัน", "ตอบกลับโรตารี่"]

        # รับ model filter (optional)
        req_data = request.get_json()
        target_models = req_data.get("models")
        if target_models:
            if isinstance(target_models, str):
                target_models = [target_models]
            target_model_clean_set = set(normalize_model(m.strip()) for m in target_models)
        else:
            target_model_clean_set = None

        # --- ดึง model ใหม่ที่ยังไม่ถูกนับ
        new_model_counts = defaultdict(int)

        for sheet_name in response_sheets:
            sheet = workbook.worksheet(sheet_name)
            values = sheet.get_all_values()
            if not values or len(values) <= 1:
                continue

            headers = values[0]
            rows = values[1:]
            model_index = next((i for i, h in enumerate(headers) if "model" in h.lower()), None)
            if model_index is None:
                continue  # ข้ามชีตที่ไม่มีหัว column model

            counter_file = os.path.join("static", f"last_response_count_{sheet_name}.txt")
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
                if len(row) > model_index:
                    model_raw = row[model_index].strip()
                    model_clean = normalize_model(model_raw)
                    if target_model_clean_set is None or model_clean in target_model_clean_set:
                        new_model_counts[model_clean] += 1

            with open(counter_file, "w") as f:
                f.write(str(current_count))

        # --- อ่านข้อมูลจากชีตหลัก
        main_data = main_sheet.get_all_values()
        header_row = main_data[0]

        model_col_index = next((i for i, h in enumerate(header_row) if "model" in h.lower()), None)
        done_col_index = next((i for i, h in enumerate(header_row) if "จำนวนทำจริง" in h.lower()), None)

        if model_col_index is None or done_col_index is None:
            return jsonify({"status": "error", "message": "ไม่พบหัวคอลัมน์ 'MODEL' หรือ 'จำนวนทำจริง'"}), 400

        summary = []

        for model_key, count in new_model_counts.items():
            matched_row_index = None

            for i in range(len(main_data) - 1, 0, -1):  # ไล่จากล่างขึ้นบน ข้าม header
                row = main_data[i]
                if len(row) > model_col_index:
                    desc_clean = normalize_model(row[model_col_index].strip())
                    if model_key == desc_clean:
                        matched_row_index = i + 1  # เพราะ Google Sheets ใช้ index เริ่มจาก 1
                        break

            if not matched_row_index:
                summary.append(f"{model_key}: ❌ ไม่พบ MODEL ในชีตหลัก")
                continue

            matched_row = main_data[matched_row_index - 1]
            old_val = matched_row[done_col_index] if len(matched_row) > done_col_index else "0"
            try:
                old_int = int(old_val) if old_val.strip().isdigit() else 0
                new_val = old_int + count
                main_sheet.update_cell(matched_row_index, done_col_index + 1, str(new_val))
                summary.append(f"{model_key}: ✅ บวก +{count} → {new_val}")
            except Exception as e:
                summary.append(f"{model_key}: ❌ Error เขียนค่าลงชีต - {str(e)}")

        if not summary:
            summary.append("⛔ ไม่มีข้อมูลใหม่")

        return jsonify({"status": "success", "message": "\n".join(summary)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
