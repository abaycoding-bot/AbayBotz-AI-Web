import streamlit as st
import requests
import time

# --- 1. CONFIG HALAMAN ---
st.set_page_config(
    page_title="AbayBotz AI | Zenith",
    page_icon="⚡",
    layout="centered"
)

# --- 2. THEME MINIMALIST SUPREME (CLEAN & ELEGANT) ---
st.markdown("""
    <style>
    /* Background Solid Dark yang Nyaman di Mata */
    .stApp {
        background-color: #05070a;
        color: #e0e6ed;
    }
    
    /* Font Space & Clean */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Judul Zenith Minimalis */
    .zenith-header {
        text-align: center;
        font-weight: 700;
        font-size: 2.8rem;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #ffffff, #505d6e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Bubble Chat Simple & Modern */
    [data-testid="stChatMessage"] {
        background-color: #0d1117 !important;
        border: 1px solid #21262d !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-bottom: 12px !important;
    }

    /* Input Bar Futuristik */
    .stChatInputContainer {
        border-top: 1px solid #30363d !important;
        background-color: #05070a !important;
    }
    
    /* Tombol Sidebar */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1f6feb;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (FITUR TAMBAHAN) ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff;'>⚡ DASHBOARD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Fitur 1: Mode Pintar
    ai_mode = st.selectbox("🎯 Pilih Mode AI", ["Standar", "Akademik (Detail)", "Kreatif (Puitis)"])
    
    # Fitur 2: Informasi Sistem
    st.info(f"Mode saat ini: **{ai_mode}**")
    
    st.markdown("---")
    if st.button("🧹 Reset Memori Sesi"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<br><p style='font-size: 0.8rem; opacity: 0.5;'>Developed by Master Abay</p>", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown("<h1 class='zenith-header'>ABAYBOTZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.5; font-size: 0.9rem;'>Intelligence in Simplicity</p>", unsafe_allow_html=True)

# Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIKA JAWABAN TEPAT & REAL-TIME ---
if prompt := st.chat_input("Tanyakan sesuatu pada saya, Master..."):
    # Modifikasi Prompt Berdasarkan Fitur Mode
    final_prompt = prompt
    if ai_mode == "Akademik (Detail)":
        final_prompt = f"Berikan jawaban yang sangat ilmiah, detail, dan sertakan poin-poin tentang: {prompt}"
    elif ai_mode == "Kreatif (Puitis)":
        final_prompt = f"Gunakan gaya bahasa yang indah dan kreatif untuk menjelaskan: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Menggunakan jalur API tercepat (Real-Time Engine)
            res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={final_prompt}", timeout=20)
            answer = res.json().get('result', "Sistem sedang memproses data berat, Master.")
            
            # Efek Mengetik Real-Time yang Sangat Halus
            for chunk in answer.split(" "):
                full_response += chunk + " "
                placeholder.markdown(full_response + "▊")
                time.sleep(0.05) # Kecepatan membaca manusia optimal
            placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except:
            st.error("Gagal menjangkau saraf pusat. Periksa koneksi internet Master.")

st.markdown("---")
st.caption("v31.0 - Focused on Precision & Speed")
        
