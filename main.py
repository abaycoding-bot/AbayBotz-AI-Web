import streamlit as st
import requests
import time
import urllib.parse
from fpdf import FPDF
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIG HALAMAN ---
st.set_page_config(page_title="AbayBotz Gemini | Ultimate", page_icon="♊", layout="centered")

# --- 2. UI DESIGN (MODERN & FAST) ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e6ed; }
    [data-testid="stChatMessage"] { 
        background: rgba(30, 31, 32, 0.7) !important; 
        border-radius: 16px !important; 
        border: 1px solid rgba(255,255,255,0.05);
    }
    .title-text { 
        text-align: center; font-weight: 800; font-size: 2.5rem;
        background: linear-gradient(120deg, #4285f4, #9b72cb);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (STABILITY CONTROL) ---
with st.sidebar:
    st.markdown("<h2 style='color: #4285f4;'>♊ SYSTEM CORE</h2>", unsafe_allow_html=True)
    st.info("Engine: Gemini 3 Flash v41.0")
    
    ai_mode = st.selectbox("🎯 Intelligence Mode:", ["Chat (Gemini Flash)", "Vision (Nano Banana)"])
    
    st.markdown("---")
    st.write("🎙️ Voice Command:")
    audio = mic_recorder(start_prompt="Bicara", stop_prompt="Kirim", key='recorder')
    
    if st.button("🧹 Clear Session"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("<h1 class='title-text'>ABAYBOTZ AI</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Optimized for Speed, Accuracy, and Stability</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIKA RESPONS TEROPTIMASI ---
if prompt := st.chat_input("Tanyakan apa saja, Master..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            if "Vision" in ai_mode:
                # Engine Nano Banana untuk Gambar
                img_url = f"https://api.vreden.web.id/api/txt2img?query={urllib.parse.quote(prompt)}"
                st.image(img_url, caption=f"Result for: {prompt}", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": f"🎨 Visualisasi '{prompt}' selesai."})
            else:
                # Engine Gemini 3 Flash - Jalur Cepat
                with st.spinner("Mengkoneksikan ke Gemini..."):
                    # Mencoba API utama
                    res = requests.get(f"https://api.vreden.web.id/api/gemini?query={prompt}", timeout=35)
                    data = res.json()
                    answer = data.get('result') or data.get('data') or "⚠️ Maaf Master, server sedang kalibrasi. Silakan ulangi."
                
                # Efek Real-Time Gemini
                full_res = ""
                for char in answer:
                    full_res += char
                    placeholder.markdown(full_res + "●")
                    time.sleep(0.005)
                placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                st.rerun()
        except Exception as e:
            st.error("⚠️ Gangguan Transmisi Jarak Jauh. Silakan kirim ulang instruksi Master.")

st.markdown("---")
st.caption("v41.0 Supreme • Stable Neural Link Activated")
