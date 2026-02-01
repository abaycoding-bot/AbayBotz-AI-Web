import streamlit as st
import requests
import time
import urllib.parse
from fpdf import FPDF
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="AbayBotz AI - Vision Engine", page_icon="🔮", layout="centered")

# --- 2. THEME DARK PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e6ed; }
    [data-testid="stChatMessage"] { background-color: #0d1117 !important; border: 1px solid #21262d !important; border-radius: 12px !important; }
    .title-text { text-align: center; font-weight: 800; font-size: 2.5rem; background: linear-gradient(90deg, #00f2ff, #bc13fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .share-btn { display: inline-block; padding: 6px 12px; background-color: #25d366; color: white; border-radius: 20px; text-decoration: none; font-size: 0.8rem; font-weight: bold; }
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

# --- 4. SIDEBAR TOOLS ---
with st.sidebar:
    st.markdown("<h2 style='color: #00f2ff;'>🛠️ CONTROL CENTER</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Fitur Voice
    st.write("🎙️ Input Suara:")
    audio = mic_recorder(start_prompt="Bicara", stop_prompt="Stop", key='recorder')
    
    st.markdown("---")
    # Fitur Ganti Mode
    ai_mode = st.selectbox("🎯 Pilih Mode AI", ["Chat (GPT-4)", "Image Generator (DALL-E)"])
    
    if st.session_state.get("messages"):
        pdf_data = export_to_pdf(st.session_state.messages)
        st.download_button("📥 Download PDF", data=pdf_data, file_name="abaybotz_history.pdf")
    
    if st.button("🧹 Clear Session"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER ---
st.markdown("<h1 class='title-text'>ABAYBOTZ AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00f2ff;'>Mode: {ai_mode}</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "http" not in message["content"]:
            encoded_text = urllib.parse.quote(f"*[AbayBotz AI]*\n{message['content']}")
            st.markdown(f'<a href="https://wa.me/?text={encoded_text}" target="_blank" class="share-btn">📲 WhatsApp Share</a>', unsafe_allow_html=True)

# --- 6. LOGIKA AI & GAMBAR ---
if prompt := st.chat_input("Ketik perintah Master..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            if ai_mode == "Image Generator (DALL-E)":
                # Jalur Saraf Pembuat Gambar
                img_url = f"https://api.vreden.web.id/api/txt2img?query={urllib.parse.quote(prompt)}"
                st.image(img_url, caption=f"Hasil Imajinasi untuk: {prompt}", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"Berhasil membuat gambar untuk: {prompt}"})
            else:
                # Jalur Saraf Chat GPT-4
                res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={prompt}", timeout=25)
                answer = res.json().get('result', "Sistem sibuk.")
                full_res = ""
                for char in answer:
                    full_res += char
                    placeholder.markdown(full_res + "▊")
                    time.sleep(0.01)
                placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                st.rerun()
        except:
            st.error("Koneksi gagal. Coba lagi, Master.")
            
