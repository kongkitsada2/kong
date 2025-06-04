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
    if "1FAIpQLSeo1i3J97g_UgqpsSjPoWJy_nCqebzc1VxBBYAG1Rb_jiIuJQ" in form_url: #ปั๊มลมไร้น้ำมัน V.6
        return {
            "วันที่": "entry.954074667",
            "ประเภทปั๊มลม": "entry.1504861747",
            "ยี่ห้อปั๊มลม": "entry.33255820",
            "MODEL": "entry.357938739",
            "ประเภทมอเตอร์": "entry.938378374",
            "กำลังมอเตอร์": "entry.716381721",
        }
    elif "1FAIpQLScWiPVLv6rcorryap4HyRZF9tPES7od-HiGWT9_MzAb3md4AA" in form_url: #ปั๊มลมลูกสูบ V.4
        return {
            "วันที่": "entry.954074667",
            "ประเภทปั๊มลม": "entry.1504861747",
            "ยี่ห้อปั๊มลม": "entry.33255820",
            "MODEL": "entry.357938739",
            "ประเภทมอเตอร์": "entry.938378374",
            "กำลังมอเตอร์": "entry.716381721",
        }
    else:
        return { #ปั๊มลมโรตารี่ V.3
            "วันที่": "entry.954074667",
            "ประเภทปั๊มลม": "entry.1504861747",
            "ยี่ห้อปั๊มลม": "entry.33255820",
            "MODEL": "entry.357938739",
            "ประเภทมอเตอร์": "entry.938378374",
            "กำลังมอเตอร์": "entry.716381721",
        }

