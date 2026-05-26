import json
import os

import gspread
from google.oauth2.service_account import Credentials


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheet():
    sheet_id = os.getenv("GOOGLE_SHEETS_ID")
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

    if not sheet_id:
        raise RuntimeError("ไม่พบ GOOGLE_SHEETS_ID")

    if service_account_json:
        service_account_info = json.loads(service_account_json)
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES,
        )
    elif service_account_file:
        credentials = Credentials.from_service_account_file(
            service_account_file,
            scopes=SCOPES,
        )
    else:
        raise RuntimeError(
            "ไม่พบ GOOGLE_SERVICE_ACCOUNT_JSON หรือ GOOGLE_SERVICE_ACCOUNT_FILE"
        )

    client = gspread.authorize(credentials)
    return client.open_by_key(sheet_id).sheet1