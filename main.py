import streamlit as st
import requests
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AbayBotz AI | The Most Powerful Assistant",
    page_icon="👑",
    layout="centered"
)

# --- 2. THEME SUPREME (UI/UX KELAS DUNIA) ---
st.markdown("""
    <style>
    /* Background Animasi Berjalan */
    .stApp {
        background: linear-gradient(-45deg, #050505, #0a192f, #1a0b2e, #000000);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Judul Dengan Efek Hologram */
    .title-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2ff, #006aff, #7000ff, #00f2ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-align: center;
        margin-bottom: 0px;
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Container Chat Mewah */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        padding: 20px;
        margin-top: 15px;
    }

    /* Efek Glow pada Input */
    .stChatInputContainer {
        border: 2px solid rgba(0, 242, 255, 0.3) !important;
        border-radius: 50px !important;
        background: rgba(0,0,0,0.8) !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 242, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (SYSTEM CORE) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00f2ff;'>CORE INTERFACE</h2>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/originals/c6/3d/8c/c63d8c3667c427042a353664d60317e0.gif") # AI Pulse Effect
    st.markdown("---")
    st.markdown("💎 **Rank:** Master")
    st.markdown("🚀 **Engine:** GPT-4o Supreme")
    st.markdown("🔋 **Efficiency:** 99.9%")
    st.markdown("---")
    if st.button("🔴 EMERGENCY RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 4. HEADER UTAMA ---
st.markdown("<h1 class='title-text'>ABAYBOTZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00f2ff; letter-spacing: 3px; font-weight: 300;'>THE ULTIMATE NEURAL ASSISTANT</p>", unsafe_allow_html=True)

# Memori Sesi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. REAL-TIME PROCESSING ---
if prompt := st.chat_input("Instruksi Anda adalah perintah bagi saya, Master..."):
    # Tampilkan pesan Master
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI dengan Efek Real-Time
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        with st.spinner("Mengkalkulasi respons terbaik..."):
            try:
                # Menghubungkan ke API Saraf Pusat
                res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={prompt}", timeout=25)
                answer = res.json().get('result', "Sistem sedang padat, Master.")
                
                # Animasi Pengetikan Halus
                for word in answer.split():
                    full_res += word + " "
                    time.sleep(0.04)
                    placeholder.markdown(full_res + "⚡")
                placeholder.markdown(full_res)
                
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error("Transmisi data terputus. Mohon periksa koneksi satelit Master.")

# --- FOOTER ---
st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>AbayBotz AI Supreme v30.0 • Secured by Master Abay</p>", unsafe_allow_html=True)
