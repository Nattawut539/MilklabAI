import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from sheets_client import get_sheet


def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print('กรุณาใส่ข้อมูลยอดขาย เช่น python sales_logger.py "ลาเต้น้ำผึ้ง:5:65"')
        return

    raw_data = sys.argv[1]

    try:
        menu, quantity, price = raw_data.split(":")

        menu = menu.strip()
        quantity = int(quantity)
        price = float(price)
        total = quantity * price

        created_at = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%Y-%m-%d %H:%M:%S")

        sheet = get_sheet()
        sheet.append_row([
            created_at,
            menu,
            quantity,
            price,
            total,
        ])

        print("✓ บันทึกยอดขายสำเร็จ")
        print(f"วันที่: {created_at}")
        print(f"เมนู: {menu}")
        print(f"จำนวน: {quantity}")
        print(f"ราคา: {price}")
        print(f"ยอดรวม: {total}")

    except ValueError:
        print("รูปแบบข้อมูลไม่ถูกต้อง")
        print('ตัวอย่างที่ถูกต้อง: python sales_logger.py "ลาเต้น้ำผึ้ง:5:65"')
    except Exception as error:
        print("เกิดข้อผิดพลาด:", error)


if __name__ == "__main__":
    main()