import streamlit as st
import requests
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AbayBotz AI | Neural Interface",
    page_icon="⚡",
    layout="centered"
)

# --- 2. CSS SUPREME (VISUAL NEON & GLASS) ---
st.markdown("""
    <style>
    /* Background Animasi Gelap */
    .stApp {
        background: radial-gradient(circle at center, #06090f 0%, #000000 100%);
    }

    /* Judul Neon Berpijar */
    .neon-text {
        font-family: 'Orbitron', sans-serif;
        color: #fff;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 40px #bc13fe;
        margin-bottom: 0px;
    }

    /* Sub-header */
    .sub-text {
        text-align: center;
        color: #00d4ff;
        font-family: 'Inter', sans-serif;
        letter-spacing: 2px;
        font-size: 0.9rem;
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* Bubble Chat Glassmorphism Luxury */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.2);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        padding: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Styling Input Box */
    .stChatInputContainer {
        border-radius: 30px;
        border: 1px solid #00d4ff;
        background: rgba(0,0,0,0.5);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #bc13fe;
    }

    /* Animasi Progress Bar */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #00d4ff, #bc13fe);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; text-align: center;'>JARVIS CORE</h1>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/originals/3d/8e/9c/3d8e9c3c138f3f88f8d689b140134764.gif") # Efek lingkaran AI bergerak
    st.markdown("---")
    st.write("💎 **User Level:** Master")
    st.write("🧠 **AI Model:** Supreme GPT-4o")
    st.write("🌐 **Status:** Online 24/7")
    st.markdown("---")
    if st.button("🚀 CLEAR SYSTEM MEMORY"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER ---
st.markdown("<h1 class='neon-text'>ABAYBOTZ</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Developed by Master Abay • Advanced Neural Network</p>", unsafe_allow_html=True)

# Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. REAL-TIME ENGINE ---
if prompt := st.chat_input("Berikan perintah, Master..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        try:
            # Panggilan API
            res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={prompt}", timeout=25)
            data = res.json().get('result', "⚠️ Kegagalan Transmisi.")
            
            # Efek Mengetik Super Mulus
            for char in data:
                full_res += char
                placeholder.markdown(full_res + "█")
                time.sleep(0.005) # Lebih cepat dan responsif
            placeholder.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except:
            st.error("Gagal terhubung ke pusat data. Pastikan koneksi stabil.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #555;'>Powering the future with AbayBotz AI Supreme</p>", unsafe_allow_html=True)
