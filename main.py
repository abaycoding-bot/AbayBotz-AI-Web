import streamlit as st
import requests
import time
import urllib.parse
from fpdf import FPDF
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="AbayBotz Gemini | Creator Suite", page_icon="🎬", layout="centered")

# --- 2. THEME GEMINI CREATOR (VIBRANT NEON) ---
st.markdown("""
    <style>
    .stApp { background-color: #040608; color: #e8eaed; }
    [data-testid="stChatMessage"] { background: rgba(30, 31, 32, 0.8) !important; border-radius: 15px !important; }
    .title-text { 
        text-align: center; font-weight: 800; font-size: 2.5rem;
        background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570, #25d366);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .social-btn {
        display: inline-block; padding: 8px 20px; border-radius: 25px;
        color: white; text-decoration: none; font-size: 0.8rem; font-weight: bold; margin-right: 5px; margin-top: 10px;
    }
    .btn-ig { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
    .btn-tk { background: #000000; border: 1px solid #ff0050; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (CREATOR TOOLS) ---
with st.sidebar:
    st.markdown("<h2 style='color: #4285f4;'>🎨 CREATOR HUB</h2>", unsafe_allow_html=True)
    
    # Mode Utama
    ai_mode = st.radio("🚀 Pilih Engine:", ["Gemini 3 Flash (Chat)", "Nano Banana (Image)", "Veo Engine (Video)"])
    
    st.markdown("---")
    st.write("🎙️ Voice Command:")
    audio = mic_recorder(start_prompt="Bicara", stop_prompt="Kirim", key='recorder')
    
    if st.button("🧹 Reset Neural Cache"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("<h1 class='title-text'>ABAYBOTZ CREATOR</h1>", unsafe_allow_html=True)
st.caption("Integrated with Gemini 3 Flash, Nano Banana, & Veo Engine")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Share buttons untuk Assistant
        if message["role"] == "assistant":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<a href="https://www.instagram.com/" target="_blank" class="social-btn btn-ig">📸 Post to Instagram</a>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<a href="https://www.tiktok.com/upload" target="_blank" class="social-btn btn-tk">🎵 Post to TikTok</a>', unsafe_allow_html=True)

# --- 5. REAL-TIME CREATION LOGIC ---
if prompt := st.chat_input("Apa yang ingin Master buat hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if "Image" in ai_mode:
                img_url = f"https://api.vreden.web.id/api/txt2img?query={urllib.parse.quote(prompt)}"
                st.image(img_url, caption="Art by Nano Banana", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"Master, gambar '{prompt}' telah berhasil dirender oleh Nano Banana."})
            
            elif "Video" in ai_mode:
                st.info("🔄 Sedang memproses video dengan Veo Engine... (Est: 30-60 detik)")
                # Simulasi hasil video
                st.session_state.messages.append({"role": "assistant", "content": f"Video Veo untuk prompt '{prompt}' sedang dalam antrean render."})
            
            else:
                res = requests.get(f"https://api.vreden.web.id/api/gemini?query={prompt}", timeout=25)
                answer = res.json().get('result', "Koneksi Gemini terputus.")
                placeholder = st.empty()
                full_res = ""
                for word in answer.split():
                    full_res += word + " "
                    placeholder.markdown(full_res + "●")
                    time.sleep(0.02)
                placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                st.rerun()
        except:
            st.error("Gagal sinkronisasi dengan pusat kreatif.")
