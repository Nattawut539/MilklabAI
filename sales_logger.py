# sales_logger.py
import sys
from datetime import datetime

from dotenv import load_dotenv

from sheets_client import get_sheet


def main():
    # โหลดค่าจากไฟล์ .env
    load_dotenv()

    # ตรวจว่าผู้ใช้ส่ง argument มาหรือยัง
    if len(sys.argv) < 2:
        print('กรุณาใส่ข้อมูลยอดขาย เช่น python sales_logger.py "ลาเต้น้ำผึ้ง:5:65"')
        return

    raw_data = sys.argv[1]

    try:
        # รูปแบบที่ต้องการ: เมนู:จำนวน:ราคา
        menu, quantity, price = raw_data.split(":")

        quantity = int(quantity)
        price = float(price)
        total = quantity * price

        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet = get_sheet()

        # เพิ่มข้อมูลลง Google Sheets
        sheet.append_row([
            today,
            menu,
            quantity,
            price,
            total
        ])

        print("✓ บันทึกยอดขายสำเร็จ")
        print(f"เมนู: {menu}")
        print(f"จำนวน: {quantity}")
        print(f"ราคา: {price}")
        print(f"ยอดรวม: {total}")

    except ValueError:
        print("รูปแบบข้อมูลไม่ถูกต้อง")
        print('ตัวอย่างที่ถูกต้อง: python sales_logger.py "ลาเต้น้ำผึ้ง:5:65"')

    except Exception as e:
        print("เกิดข้อผิดพลาด:", e)


if __name__ == "__main__":
    main()