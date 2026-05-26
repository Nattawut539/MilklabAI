# morning_report.py
import os
import requests
from datetime import datetime, timedelta
from collections import defaultdict

from dotenv import load_dotenv
from sheets_client import get_sheet


def send_telegram_message(message: str):
    """ส่งข้อความไป Telegram"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token:
        raise RuntimeError("ไม่พบ TELEGRAM_BOT_TOKEN ใน .env")

    if not chat_id:
        raise RuntimeError("ไม่พบ TELEGRAM_CHAT_ID ใน .env")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=15,
    )

    if response.status_code != 200:
        raise RuntimeError(f"ส่ง Telegram ไม่สำเร็จ: {response.text}")

    return response.json()


def main():
    load_dotenv()

    sheet = get_sheet()
    rows = sheet.get_all_records()

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    total_sales = 0
    menu_count = defaultdict(int)
    found_rows = []

    for row in rows:
        # ชื่อคอลัมน์ต้องตรงกับหัวตารางใน Google Sheet
        date_text = str(row.get("วันที่", ""))
        menu = str(row.get("เมนู", ""))
        quantity = int(row.get("จำนวน", 0) or 0)
        total = float(row.get("ยอดรวม", 0) or 0)

        # sales_logger.py บันทึกวันที่เป็น YYYY-MM-DD HH:MM:SS
        # เลยใช้ startswith เพื่อเทียบเฉพาะวันที่
        if date_text.startswith(yesterday):
            found_rows.append(row)
            total_sales += total
            menu_count[menu] += quantity

    if not found_rows:
        message = (
            "☀️ Morning Report Milk Mate\n\n"
            f"วันที่สรุป: {yesterday}\n"
            "เมื่อวานยังไม่มีข้อมูลยอดขายใน Google Sheets น้า 🥛"
        )
    else:
        best_menu = max(menu_count, key=menu_count.get)
        best_quantity = menu_count[best_menu]

        message = (
            "☀️ Morning Report Milk Mate\n\n"
            f"วันที่สรุป: {yesterday}\n"
            f"ยอดขายรวมเมื่อวาน: {total_sales:,.2f} บาท\n"
            f"เมนูขายดีที่สุด: {best_menu}\n"
            f"ขายได้ทั้งหมด: {best_quantity} แก้ว\n\n"
            "ขอให้วันนี้ขายดีเหมือนเดิมนะ 🥛✨"
        )

    print(message)
    send_telegram_message(message)
    print("✓ ส่ง Morning Report ไปที่ Telegram สำเร็จ")


if __name__ == "__main__":
    main()