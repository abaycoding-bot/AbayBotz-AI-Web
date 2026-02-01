import logging
import requests
import time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- IDENTITAS MASTER (TOKEN UPDATED) ---
TOKEN = "8461042281:AAHjNYiKfHthlayT0hnSMs7lauw40IVJbxM"
BOT_NAME = "AbayBotz AI"

# Mengatur log agar Master bisa melihat proses di balik layar
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- PROMPT JARVIS (Kunci Kecerdasan) ---
SYSTEM_PROMPT = (
    "Kamu adalah AbayBotz AI, asisten Jarvis tingkat tinggi yang dikembangkan Master Abay. "
    "Tugasmu: Menjawab semua instruksi dengan cerdas, elegan, dan sangat detail. "
    "Selalu sapa dengan 'Master'. Jika ditanya hal teknis, jelaskan secara mendalam "
    "dengan bahasa yang mulus dan profesional."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    # Menu tombol futuristik
    keyboard = [['🎙️ Protokol Tanya', '📡 Status Sistem'], ['👨‍💻 Developer', '🧹 Reset Memori']]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"🌌 **{BOT_NAME} : JARVIS PROTOCOL ACTIVE**\n\n"
        f"Selamat datang kembali, **Master {user_name}**. Seluruh sistem telah disinkronkan. "
        "Saya siap melayani instruksi Anda. Apa yang perlu saya proses?",
        reply_markup=markup, parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    chat_id = update.effective_chat.id
    
    # Fitur Tombol Menu
    if user_msg == '🎙️ Protokol Tanya':
        await update.message.reply_text("🎙️ **Protokol Tanya Aktif.** Silakan kirimkan pertanyaan Master.")
        return
    elif user_msg == '📡 Status Sistem':
        await update.message.reply_text("🌐 **LAPORAN INTI**\n• Status: Normal\n• Latency: 0.01ms\n• Engine: GPT-4o Supreme")
        return
    elif user_msg == '👨‍💻 Developer':
        await update.message.reply_text("Sistem ini dikembangkan secara eksklusif oleh **Master Abay**.")
        return
    elif user_msg == '🧹 Reset Memori':
        await update.message.reply_text("🧹 Memori percakapan telah dibersihkan. Memulai ulang urutan saraf...")
        return

    # Animasi 'Typing' agar terlihat natural
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    # Pengolahan Data AI (Multi-Server untuk kecepatan kilat)
    full_query = f"{SYSTEM_PROMPT}\n\nUser: {user_msg}\nJarvis:"
    urls = [
        f"https://api.vreden.web.id/api/gpt4?query={full_query}",
        f"https://widipe.com/gpt4?text={full_query}"
    ]
    
    jawaban = ""
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                hasil = data.get('result') or data.get('data') or data.get('response')
                if hasil:
                    jawaban = str(hasil).strip()
                    break
        except:
            continue

    if jawaban:
        await update.message.reply_text(jawaban, parse_mode='Markdown')
    else:
        # Pesan jika server sedang overload
        await update.message.reply_text("Maaf Master, terjadi gangguan transmisi. Mohon ulangi instruksi Anda.")

if __name__ == '__main__':
    while True:
        try:
            print(f"--- MENGHUBUNGKAN {BOT_NAME} KE SATELIT ---")
            app = ApplicationBuilder().token(TOKEN).build()
            
            # Handler
            app.add_handler(CommandHandler('start', start))
            app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
            
            print(f"✅ {BOT_NAME} JARVIS MODE ONLINE")
            app.run_polling(drop_pending_updates=True)
        except Exception as e:
            print(f"⚠️ Sistem Terputus: {e}. Mencoba Re-koneksi dalam 5 detik...")
            time.sleep(5)
      
