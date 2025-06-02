#แก้ google sheet ด้วย
#เปลี่ยน entry.id ที่ได้จาก google form แบบกรอกฟอร์มล่วงหน้า
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

def get_entry_mapping_by_form_url(form_url):
    if "Sf3ezCVJrYeW9txzxs1THloSflxCdm12_L19ghfru-9XQ4Mvg" in form_url:
        return {
            "วันที่": "entry.1479110611",
            "ประเภทปั๊มลม": "entry.2058113853",
            "ยี่ห้อปั๊มลม": "entry.713069193",
            "MODEL": "entry.347733934",
            "ประเภทมอเตอร์": "entry.2103516068",
            "กำลังมอเตอร์": "entry.1794014403",
        }
    elif "1FAIpQLScHgJjqFkxZJ5K_TfinnzNGS9taeqlVAR4SnMWDBSoTwNmFVA" in form_url:
        return {
            "วันที่": "entry.1616411344",
            "ประเภทปั๊มลม": "entry.1661700905",
            "ยี่ห้อปั๊มลม": "entry.615767597",
            "MODEL": "entry.1573106649",
            "ประเภทมอเตอร์": "entry.1547661818",
            "กำลังมอเตอร์": "entry.431007909",
        }
    else:
        return {
            "วันที่": "entry.1301553690",
            "ประเภทปั๊มลม": "entry.1683658413",
            "MODEL": "entry.1159901527",
            "ยี่ห้อปั๊มลม": "entry.139507719",
            "ประเภทมอเตอร์": "entry.1101246079",
            "กำลังมอเตอร์": "entry.1774963468",
        }

