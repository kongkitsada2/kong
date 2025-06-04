#แก้ google sheet ด้วย
#เปลี่ยน entry.id ที่ได้จาก google form แบบกรอกฟอร์มล่วงหน้า
import json, os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
json_creds = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
client = gspread.authorize(creds)

def get_entry_mapping_by_form_url(form_url):
    if "1MolkOjNwwqc09wtdo-l-o3mBB5z3kb86nGe7a1eCdIc" in form_url: #ปั๊มลมไร้น้ำมัน V.6
        return {
            "วันที่": "entry.954074667",
            "ประเภทปั๊มลม": "entry.1504861747",
            "ยี่ห้อปั๊มลม": "entry.33255820",
            "MODEL": "entry.357938739",
            "ประเภทมอเตอร์": "entry.938378374",
            "กำลังมอเตอร์": "entry.716381721",
        }
    elif "1U9GR1gg42X5B3I3inL6UNIS5wYh4kEz6LKxsUnh1yng" in form_url: #ปั๊มลมลูกสูบ V.4
        return {
            "วันที่": "entry.954074667",
            "ประเภทปั๊มลม": "entry.1504861747",
            "ยี่ห้อปั๊มลม": "entry.33255820",
            "MODEL": "entry.357938739",
            "ประเภทมอเตอร์": "entry.938378374",
            "กำลังมอเตอร์": "entry.716381721",
        }
    elif "1V--MTqozy5pfAImoIevYhgPL1e7BZQv9G0zYrO-Mq7c" in form_url: #ปั๊มลมโรตารี่ V.3
        return { 
            "วันที่": "entry.954074667",
            "ประเภทปั๊มลม": "entry.1504861747",
            "ยี่ห้อปั๊มลม": "entry.33255820",
            "MODEL": "entry.357938739",
            "ประเภทมอเตอร์": "entry.938378374",
            "กำลังมอเตอร์": "entry.716381721",
        }

