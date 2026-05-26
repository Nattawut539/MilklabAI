# agent_tools.py
from datetime import datetime
from zoneinfo import ZoneInfo


def validate_sale(menu: str, quantity: int, price: float) -> None:
    """
    Guardrails:
    ตรวจสอบข้อมูลก่อนบันทึกยอดขาย
    ถ้าข้อมูลไม่ถูกต้อง ให้ raise ValueError
    """

    if not menu or not menu.strip():
        raise ValueError("ชื่อเมนูห้ามว่าง")

    if quantity <= 0:
        raise ValueError("จำนวนต้องมากกว่า 0")

    if price <= 0:
        raise ValueError("ราคาต้องมากกว่า 0")


def log_sale(menu: str, quantity: int, price: float) -> dict:
    """
    Tool สำหรับบันทึกยอดขาย
    ตอนนี้เป็น fake result ก่อน ยังไม่ได้ต่อ Google Sheets
    """

    validate_sale(menu, quantity, price)

    total = quantity * price
    timestamp = datetime.now(ZoneInfo("Asia/Bangkok")).isoformat()

    return {
        "status": "success",
        "menu": menu.strip(),
        "quantity": quantity,
        "price": price,
        "total": total,
        "timestamp": timestamp,
    }


TOOLS = {
    "log_sale": log_sale,
}