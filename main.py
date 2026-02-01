import streamlit as st
import requests

# KONFIGURASI WEBSITE
st.set_page_config(page_title="AbayBotz AI", page_icon="🤖")

st.title("🤖 AbayBotz AI Supreme")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Apa instruksi Anda, Master?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Berpikir..."):
            try:
                # Menghubungkan ke jalur saraf AI
                res = requests.get(f"https://api.vreden.web.id/api/gpt4?query={prompt}", timeout=15)
                jawaban = res.json().get('result', "Sistem sibuk.")
                st.markdown(jawaban)
                st.session_state.messages.append({"role": "assistant", "content": jawaban})
            except:
                st.error("Koneksi satelit terputus.")
                
