# sheets_client.py
import json
import os

import gspread
from google.oauth2.service_account import Credentials


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheet():
    """
    เชื่อมต่อ Google Sheets

    รองรับ 2 แบบ:
    1. รันใน Codespaces / เครื่องเรา ใช้ GOOGLE_SERVICE_ACCOUNT_FILE
    2. รันใน GitHub Actions ใช้ GOOGLE_SERVICE_ACCOUNT_JSON
    """

    json_str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    file_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    sheet_id = os.getenv("GOOGLE_SHEETS_ID")

    if not sheet_id:
        raise RuntimeError("ไม่พบ GOOGLE_SHEETS_ID ใน .env")

    if json_str:
        # ใช้ตอนรันบน GitHub Actions
        info = json.loads(json_str)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)

    elif file_path:
        # ใช้ตอนรันใน Codespaces / local
        creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)

    else:
        raise RuntimeError(
            "ไม่พบ GOOGLE_SERVICE_ACCOUNT_JSON หรือ GOOGLE_SERVICE_ACCOUNT_FILE"
        )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1

    return sheet