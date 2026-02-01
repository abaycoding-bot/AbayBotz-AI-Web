import streamlit as st
import requests
import time
import urllib.parse
from fpdf import FPDF
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="AbayBotz AI | Supreme Social", page_icon="🌐", layout="centered")

# --- 2. THEME SUPREME (DARK & NEON) ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e6ed; }
    [data-testid="stChatMessage"] { background-color: #0d1117 !important; border: 1px solid #21262d !important; border-radius: 12px !important; }
    .title-text { text-align: center; font-weight: 700; font-size: 2.5rem; background: linear-gradient(90deg, #00f2ff, #bc13fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .share-btn { display: inline-block; padding: 5px 15px; background-color: #25d366; color: white; border-radius: 20px; text-decoration: none; font-size: 0.8rem; font-weight: bold; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI PDF ---
def export_to_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AbayBotz AI - Chat History", ln=1, align='C')
    for msg in chat_history:
        role = "Master" if msg["role"] == "user" else "AbayBotz"
        pdf.multi_cell(0, 10, txt=f"{role}: {msg['content']}")
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SIDEBAR (VOICE & TOOLS) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00f2ff;'>🎙️ VOICE COMMAND</h2>", unsafe_allow_html=True)
    audio = mic_recorder(start_prompt="Bicara Sekarang", stop_prompt="Selesai", key='recorder')
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Dokumen Analisis", type=['txt'])
    ai_mode = st.selectbox("🎯 Mode Sistem", ["Standar", "Akademik", "Kreatif"])
    
    if st.session_state.get("messages"):
        pdf_data = export_to_pdf(st.session_state.messages)
        st.download_button("📥 Download PDF", data=pdf_data, file_name="abaybotz_chat.pdf")
    
    if st.button("🧹 Clear Session"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER ---
st.markdown("<h1 class='title-text'>ABAYBOTZ AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Tambahkan Tombol Share WhatsApp jika itu pesan dari AI
        if message["role"] == "assistant":
            encoded_text = urllib.parse.quote(f"*[AbayBotz AI]* \n\n{message['content']}")
            st.markdown(f'<a href="https://wa.me/?text={encoded_text}" target="_blank" class="share-btn">📲 Share to WhatsApp</a>', unsafe_allow_html=True)

# --- 6. LOGIKA INPUT ---
input_text = st.chat_input("Tanyakan sesuatu pada Jarvis...")
prompt = input_text # Suara akan masuk ke input_text pada update sistem browser selanjutnya

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        try:
            res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={prompt}", timeout=25)
            answer = res.json().get('result', "Koneksi satelit sibuk.")
            for word in answer.split(" "):
                full_res += word + " "
                placeholder.markdown(full_res + "▊")
                time.sleep(0.04)
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun() # Refresh agar tombol share muncul
        except:
            st.error("Gagal terhubung.")
        
