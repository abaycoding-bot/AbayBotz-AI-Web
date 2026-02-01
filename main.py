import streamlit as st
import requests
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AbayBotz AI - Jarvis",
    page_icon="🤖",
    layout="centered"
)

# --- 2. STYLE CSS CUSTOM (Tampilan AI Modern) ---
st.markdown("""
    <style>
    /* Mengubah background utama */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Header styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #00D4FF;
        text-align: center;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Chat Bubble styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #161B22;
    }
    
    /* Input Box styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (MENU SAMPING) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("AbayBotz AI")
    st.subheader("Sistem Jarvis v27.0")
    st.markdown("---")
    st.info("Asisten digital cerdas yang dikembangkan oleh **Master Abay** untuk membantu produktivitas.")
    if st.button("🧹 Bersihkan Percakapan"):
        st.session_state.messages = []
        st.rerun()

# --- 4. AREA CHAT ---
st.markdown("<h1 class='main-header'>AbayBotz AI</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center; color: #8B949E;'>Sistem Kecerdasan Buatan Terintegrasi</p>", unsafe_allow_html=True)

# Inisialisasi memori chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat dengan gelembung percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIKA INPUT & RESPONS ---
if prompt := st.chat_input("Tulis instruksi Anda di sini, Master..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respons AI
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Menghubungkan ke satelit pengolah data..."):
            try:
                # Memanggil Jalur Saraf AI
                res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={prompt}", timeout=20)
                answer = res.json().get('result', "Maaf Master, transmisi terganggu.")
                
                # Efek mengetik mulus (Typewriter effect)
                for word in answer.split():
                    full_response += word + " "
                    time.sleep(0.05)
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Kegagalan sistem: {e}")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("© 2026 Developed by Master Abay | Powered by GPT-4 Supreme")
            
                
