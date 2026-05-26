# agent_harness.py
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from google import genai

from agent_tools import TOOLS


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError("ไม่พบ GOOGLE_API_KEY ในไฟล์ .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """
คุณคือ Demi ผู้ช่วย AI ของร้าน Milk Mate
หน้าที่ของคุณคือแปลงคำสั่งภาษาไทยเป็น JSON action เท่านั้น

ตอบกลับเป็น JSON เท่านั้น ห้ามมีคำอธิบายอื่น

รูปแบบที่ถูกต้อง:
{"action": "log_sale", "args": {"menu": "...", "quantity": N, "price": N}}

กฎ:
- ถ้าผู้ใช้ต้องการบันทึกยอดขาย ให้ใช้ action เป็น "log_sale"
- menu คือชื่อเมนู
- quantity คือจำนวนสินค้า เป็นตัวเลข
- price คือราคาต่อหน่วย เป็นตัวเลข
- ถ้าคำสั่งไม่ใช่การบันทึกยอดขาย ให้ตอบ:
{"action": "unknown", "args": {}}
"""

TRACE_FILE = "agent_trace.log"


def now_bangkok() -> str:
    """คืนค่าเวลาปัจจุบันตามเวลาไทย"""
    return datetime.now(ZoneInfo("Asia/Bangkok")).isoformat()


def write_trace(event: str, data: dict) -> None:
    """
    เขียน trace log เพื่อดูว่า agent รับ input อะไร
    LLM ตอบอะไร และ tool ได้ผลลัพธ์อะไร
    """

    record = {
        "timestamp": now_bangkok(),
        "event": event,
        **data,
    }

    with open(TRACE_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def extract_json(raw_text: str) -> dict:
    """
    แปลงข้อความจาก AI เป็น JSON
    กันกรณี AI เผลอใส่ ```json ครอบมา
    """

    cleaned = raw_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "", 1).strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "", 1).strip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    return json.loads(cleaned)


def run_agent(user_input: str) -> str:
    """
    รับคำสั่งผู้ใช้ → ให้ Gemini แปลงเป็น JSON action
    → ตรวจ action → เรียก tool → ส่งข้อความผลลัพธ์กลับ
    """

    write_trace("user_input", {"message": user_input})

    response = client.models.generate_content(
        model=MODEL,
        contents=f"{SYSTEM_INSTRUCTION}\n\nคำสั่ง: {user_input}",
    )

    raw = response.text.strip()
    write_trace("llm_response", {"raw": raw})

    try:
        action_data = extract_json(raw)
    except json.JSONDecodeError:
        write_trace("json_error", {"raw": raw})
        return "❌ AI ตอบกลับในรูปแบบ JSON ไม่ถูกต้อง"

    action = action_data.get("action")
    args = action_data.get("args", {})

    if action == "unknown":
        write_trace("unknown_action", {"action": action, "args": args})
        return "⚠️ คำสั่งนี้ไม่ใช่การบันทึกยอดขาย"

    if action not in TOOLS:
        write_trace("invalid_action", {"action": action, "args": args})
        return f"⚠️ ไม่รู้จัก action: {action}"

    try:
        result = TOOLS[action](**args)

        write_trace(
            "tool_result",
            {
                "action": action,
                "args": args,
                "result": result,
            },
        )

        return (
            f"✅ บันทึกสำเร็จ: {result['menu']} "
            f"x{result['quantity']} = {result['total']} บาท"
        )

    except (ValueError, TypeError) as error:
        write_trace(
            "tool_error",
            {
                "action": action,
                "args": args,
                "error": str(error),
            },
        )

        return f"❌ ข้อมูลไม่ถูกต้อง: {error}"


if __name__ == "__main__":
    print("Demi Agent พร้อมรับคำสั่ง")
    print("พิมพ์ 'exit' เพื่อออก\n")

    while True:
        user_input = input("คุณ: ").strip()

        if user_input.lower() == "exit":
            print("Demi: แล้วเจอกันใหม่นะ 🥛")
            break

        if not user_input:
            print("Demi: กรุณาพิมพ์คำสั่งก่อนนะ\n")
            continue

        print(f"Demi: {run_agent(user_input)}\n")