# app.py
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from rag_engine import RAGEngine


# =========================
# Config
# =========================
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-2.5-flash"

st.set_page_config(
    page_title="MilkLab° Demi AI",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# Custom CSS
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Prompt', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 182, 193, 0.35), transparent 30%),
            radial-gradient(circle at top right, rgba(173, 216, 230, 0.35), transparent 30%),
            linear-gradient(135deg, #fff7fb 0%, #f5fbff 45%, #fffdf4 100%);
    }

    .main-header {
        padding: 28px 30px;
        border-radius: 28px;
        background: linear-gradient(135deg, #ff8fab 0%, #ffc2d1 45%, #bde0fe 100%);
        box-shadow: 0 18px 45px rgba(255, 143, 171, 0.28);
        margin-bottom: 24px;
        color: white;
    }

    .main-header h1 {
        font-size: 42px;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .main-header p {
        margin-top: 10px;
        font-size: 17px;
        opacity: 0.95;
    }

    .glass-card {
        padding: 22px;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.75);
        box-shadow: 0 16px 40px rgba(80, 80, 120, 0.12);
        backdrop-filter: blur(12px);
        margin-bottom: 18px;
    }

    .status-pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.65);
        color: #5b5b7a;
        font-size: 14px;
        margin-right: 8px;
        margin-top: 8px;
        border: 1px solid rgba(255, 255, 255, 0.9);
    }

    .mini-title {
        font-weight: 700;
        font-size: 20px;
        color: #34344a;
        margin-bottom: 8px;
    }

    .mini-text {
        color: #666680;
        font-size: 15px;
        line-height: 1.7;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff1f6 0%, #eef7ff 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.7);
    }

    .chat-box {
        border-radius: 24px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.62);
        box-shadow: 0 12px 30px rgba(100, 100, 140, 0.10);
    }

    div[data-testid="stChatMessage"] {
        border-radius: 22px;
        padding: 10px 14px;
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 8px 22px rgba(80, 80, 120, 0.08);
    }

    .stButton > button {
        border-radius: 999px;
        border: none;
        background: linear-gradient(135deg, #ff8fab, #bde0fe);
        color: white;
        font-weight: 600;
        padding: 10px 18px;
        transition: 0.2s ease;
        box-shadow: 0 8px 18px rgba(255, 143, 171, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(255, 143, 171, 0.35);
    }

    .stChatInput {
        border-radius: 999px;
    }

    .footer-note {
        text-align: center;
        color: #777790;
        font-size: 13px;
        margin-top: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Load RAG
# =========================
@st.cache_resource
def load_rag():
    return RAGEngine("knowledge/milklab_kb.txt")


def get_gemini_client():
    if not GOOGLE_API_KEY:
        return None
    return genai.Client(api_key=GOOGLE_API_KEY)


rag = load_rag()
client = get_gemini_client()


# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("## 🥛 MilkLab°")
    st.markdown(
        """
        **Demi AI** ผู้ช่วยตอบคำถามร้านนม  
        ใช้ระบบ RAG ค้นข้อมูลจาก Knowledge Base ก่อนตอบ
        """
    )

    st.markdown("---")
    st.markdown("### ✨ ตัวอย่างคำถาม")

    example_questions = [
        "ร้านเปิดกี่โมง",
        "มีเมนูอะไรบ้าง",
        "ลาเต้น้ำผึ้งมีน้ำตาลไหม",
        "Delivery ได้ไหม",
        "ร้านอยู่ที่ไหน",
    ]

    selected_example = None

    for question in example_questions:
        if st.button(question, use_container_width=True):
            selected_example = question

    st.markdown("---")
    st.markdown("### 🔐 Status")

    if GOOGLE_API_KEY:
        st.success("เชื่อมต่อ GOOGLE_API_KEY แล้ว")
    else:
        st.error("ยังไม่ได้ตั้งค่า GOOGLE_API_KEY")


# =========================
# Header
# =========================
st.markdown(
    """
    <div class="main-header">
        <h1>🥛 Demi AI for MilkLab°</h1>
        <p>แชทบอทร้านนมสไตล์ Gen Z ตอบจากข้อมูลร้านจริง ไม่มั่ว ไม่แต่งเพิ่ม</p>
        <span class="status-pill">RAG Chatbot</span>
        <span class="status-pill">Streamlit</span>
        <span class="status-pill">Gemini</span>
        <span class="status-pill">FAISS Search</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# Intro Cards
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="glass-card">
            <div class="mini-title">📚 Knowledge Base</div>
            <div class="mini-text">
                เก็บข้อมูลเมนู ราคา เวลาเปิดร้าน ที่ตั้ง และ FAQ ของร้าน
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="glass-card">
            <div class="mini-title">🔎 RAG Search</div>
            <div class="mini-text">
                ค้นหาข้อมูลที่เกี่ยวข้องกับคำถามก่อนส่งให้ AI ตอบ
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="glass-card">
            <div class="mini-title">🤖 Demi AI</div>
            <div class="mini-text">
                ตอบลูกค้าแบบสุภาพ เข้าใจง่าย และอิงข้อมูลร้านเท่านั้น
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Chat State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "สวัสดีครับ 👋 ผมคือ Demi AI ของ MilkLab° ถามเรื่องเมนู เวลาเปิดร้าน หรือข้อมูลร้านได้เลยครับ",
        }
    ]


# =========================
# Chat Display
# =========================
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Chat Logic
# =========================
user_input = st.chat_input("พิมพ์คำถามเกี่ยวกับ MilkLab° ได้เลย...")

if selected_example:
    user_input = selected_example

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Demi กำลังค้นข้อมูลร้านให้นะครับ..."):
            if client is None:
                answer = "ยังไม่ได้ตั้งค่า GOOGLE_API_KEY ครับ กรุณาเพิ่ม API Key ในไฟล์ .env หรือ HuggingFace Secrets ก่อนใช้งาน"
            else:
                try:
                    context_chunks = rag.search(user_input, top_k=3)
                    context = "\n---\n".join(context_chunks)

                    full_prompt = f"""
คุณคือ Demi ผู้ช่วย AI ของร้าน MilkLab°
หน้าที่ของคุณคือช่วยตอบคำถามลูกค้าโดยอ้างอิงจากข้อมูลร้านเท่านั้น

กฎการตอบ:
1. ตอบเป็นภาษาไทย
2. ตอบสุภาพ เป็นกันเอง เหมาะกับร้านนมสไตล์วัยรุ่น
3. ห้ามแต่งข้อมูลเอง
4. ถ้าไม่มีข้อมูลใน context ให้ตอบว่า "ขอโทษครับ ข้อมูลนี้ยังไม่มีในระบบของร้าน"
5. ถ้าผู้ใช้ถามนอกเรื่องร้าน ให้ปฏิเสธอย่างสุภาพ แล้วชวนกลับมาถามเรื่องเมนูหรือข้อมูลร้าน

ข้อมูลร้าน:
{context}

คำถามลูกค้า:
{user_input}
"""

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=full_prompt,
                    )

                    answer = response.text

                except Exception as error:
                    answer = f"เกิดข้อผิดพลาดระหว่างเรียกใช้งาน AI: {error}"

            st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# =========================
# Footer
# =========================
st.markdown(
    """
    <div class="footer-note">
        Made with 🥛 by MilkLab° | RAG + Gemini + Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)