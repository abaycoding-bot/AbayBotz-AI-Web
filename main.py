import streamlit as st
import requests
import time
import urllib.parse
from fpdf import FPDF
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="AbayBotz Gemini | Intelligence", page_icon="♊", layout="centered")

# --- 2. UI CLEAN & MODERN ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e6ed; }
    [data-testid="stChatMessage"] { background: rgba(30, 31, 32, 0.7) !important; border-radius: 15px !important; border: 1px solid rgba(255,255,255,0.1); }
    .title-text { 
        text-align: center; font-weight: 800; font-size: 2.5rem;
        background: linear-gradient(90deg, #4285f4, #9b72cb);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (ESSENTIAL TOOLS ONLY) ---
with st.sidebar:
    st.markdown("<h2 style='color: #4285f4;'>♊ CORE SYSTEM</h2>", unsafe_allow_html=True)
    ai_mode = st.selectbox("🎯 Pilih Mode:", ["Gemini 3 Flash (Tanya Jawab)", "Nano Banana (Buat Gambar)"])
    
    st.markdown("---")
    st.write("🎙️ Voice Command:")
    audio = mic_recorder(start_prompt="Bicara", stop_prompt="Kirim", key='recorder')
    
    if st.button("🧹 Bersihkan Memori"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("<h1 class='title-text'>ABAYBOTZ AI</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Powered by Gemini 3 Flash & Nano Banana</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIKA SISTEM (SINKRONISASI TOTAL) ---
if prompt := st.chat_input("Apa yang ingin Master tanyakan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            if "Gambar" in ai_mode:
                # Engine Nano Banana untuk gambar
                img_url = f"https://api.vreden.web.id/api/txt2img?query={urllib.parse.quote(prompt)}"
                st.image(img_url, caption=f"Art for: {prompt}", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"🎨 Gambar untuk '{prompt}' berhasil dibuat."})
            else:
                # Jalur Saraf Gemini 3 Flash
                # Menggunakan API cadangan jika koneksi utama sibuk
                res = requests.get(f"https://api.vreden.web.id/api/gemini?query={prompt}", timeout=30)
                answer = res.json().get('result', "Maaf Master, transmisi otak Gemini sedang padat. Coba ulangi pertanyaan Master.")
                
                full_res = ""
                for word in answer.split():
                    full_res += word + " "
                    placeholder.markdown(full_res + "●")
                    time.sleep(0.01)
                placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                st.rerun()
        except Exception as e:
            st.error(f"⚠️ Kegagalan Sinkronisasi: {e}")
        
