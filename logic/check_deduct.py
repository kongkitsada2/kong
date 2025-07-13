import os
import re
from flask import jsonify, request
from collections import defaultdict
from utils.gsheet import client

# ---------- helper ----------------------------------------------------------
def normalize_model(text: str) -> str:
    """ทำให้ชื่อ MODEL เป็นตัวพิมพ์ใหญ่-ติดกัน (ลบเว้นวรรค – () -)"""
    return re.sub(r'[\s\-\(\)]', '', text.upper())

# ---------- main ------------------------------------------------------------
def check_and_deduct_logic():
    try:
        # --- 1) เปิด Google Sheet ------------------------------------------------
        sheet_url = (
            "https://docs.google.com/spreadsheets/d/"
            "1bief199t8kf8vV9NoAUl_sakTTBTne5tKbXW8z65TcQ/edit"
        )
        workbook     = client.open_by_url(sheet_url)
        main_sheet   = workbook.worksheet("รายงานผลQCรายวัน")
        response_sheets = ["ตอบกลับลูกสูบ", "ตอบกลับไร้น้ำมัน", "ตอบกลับโรตารี่"]

        # --- 2) รับตัวกรอง MODEL (ถ้ามี) -----------------------------------------
        body = request.get_json(silent=True) or {}
        target_models = body.get("models")
        model_filter = (
            {normalize_model(m) for m in (target_models if isinstance(target_models, list) else [target_models])}
            if target_models else None
        )

        # --- 3) เก็บ count MODEL ใหม่จากทุกชีตตอบกลับ --------------------------
        new_model_counts = defaultdict(int)

        for sheet_name in response_sheets:
            ws      = workbook.worksheet(sheet_name)
            values  = ws.get_all_values()
            if len(values) <= 1:
                continue

            headers     = values[0]
            rows        = values[1:]
            model_idx   = next((i for i, h in enumerate(headers) if "model" in h.lower()), None)
            if model_idx is None:
                continue

            counter_f = os.path.join("static", f"last_response_count_{sheet_name}.txt")
            last_cnt  = 0
            if os.path.exists(counter_f):
                try:
                    last_cnt = int(open(counter_f).read().strip())
                except ValueError:
                    pass

            for row in rows[last_cnt:]:
                if len(row) > model_idx:
                    mod_clean = normalize_model(row[model_idx])
                    if model_filter is None or mod_clean in model_filter:
                        new_model_counts[mod_clean] += 1

            # อัปเดตไฟล์ counter
            with open(counter_f, "w") as f:
                f.write(str(len(rows)))

        # --- 4) เตรียม index ของคอลัมน์ในชีตหลัก ------------------------------
        main_data  = main_sheet.get_all_values()
        headers    = main_data[0]

        model_col  = next((i for i, h in enumerate(headers) if "model"         in h.lower()), None)
        done_col   = next((i for i, h in enumerate(headers) if "จำนวนทำจริง"    in h.lower()), None)
        remain_col = next((i for i, h in enumerate(headers) if "คงเหลือ"        in h.lower()), None)

        if None in (model_col, done_col, remain_col):
            return jsonify({"status": "error",
                            "message": "ไม่พบหัวคอลัมน์ MODEL / จำนวนทำจริง / คงเหลือ"}), 400

        # --- 5) บวกค่าลง “จำนวนทำจริง” ถ้า ‘คงเหลือ’ > 0 ------------------------
        summary = []

        for mod_key, add_cnt in new_model_counts.items():
            row_to_update = None

            # ไล่จากล่างขึ้นบน
            for r in range(len(main_data) - 1, 0, -1):
                mod_in_row = normalize_model(main_data[r][model_col]) if len(main_data[r]) > model_col else ""
                if mod_in_row == mod_key:
                    # เช็กคงเหลือ
                    remain_val = main_data[r][remain_col] if len(main_data[r]) > remain_col else "0"
                    try:
                        remain_int = int(remain_val.strip())
                    except ValueError:
                        remain_int = 0

                    if remain_int <= 0:
                        summary.append(f"{mod_key}: ⚠️ คงเหลือ {remain_int} ไม่บวกเพิ่ม")
                        break

                    row_to_update = r
                    break

            if row_to_update is None:
                summary.append(f"{mod_key}: ❌ ไม่พบ MODEL ในชีตหลัก")
                continue

            # ค่าปัจจุบัน
            done_val = main_data[row_to_update][done_col] if len(main_data[row_to_update]) > done_col else "0"
            try:
                done_int = int(done_val.strip())
            except ValueError:
                done_int = 0

            new_val = done_int + add_cnt
            # Google Sheet index เริ่ม 1
            main_sheet.update_cell(row_to_update + 1, done_col + 1, str(new_val))
            summary.append(f"{mod_key}: ✅ บวก +{add_cnt} → {new_val}")

        if not summary:
            summary.append("⛔ ไม่มีข้อมูลใหม่")

        return jsonify({"status": "success", "message": "\n".join(summary)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
