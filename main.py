import os
import psycopg2
import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Biar folder project kebaca
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load mesin dari file lu yang lain
from brain import tanya_groq
from tools import dapet_waktu_sekarang

# Ambil Variables dari Railway
TOKEN_TELE = os.getenv("TOKEN_TELE")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- KONEKSI DATABASE (OTAK GAJAH) ---
def get_db_connection():
    # Gunakan koneksi SSL agar aman di Railway
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS brain_data (
                id SERIAL PRIMARY KEY,
                materi TEXT NOT NULL,
                kategori TEXT
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Otak Gajah (Database) Siap!")
    except Exception as e:
        print(f"❌ Gagal inisialisasi database: {e}")

# --- FITUR /belajar ---
async def belajar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    materi_baru = " ".join(context.args)
    if not materi_baru:
        await update.message.reply_text("Kasih materinya dong Cok! Contoh: /belajar Gold itu sideways kalo gak ada news.")
        return

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO brain_data (materi, kategori) VALUES (%s, %s)", (materi_baru, "umum"))
        conn.commit()
        cur.close()
        conn.close()
        await update.message.reply_text("Siap Bos! Ilmu baru udah gue simpen di database. Makin gacor nih! 🧠🔥")
    except Exception as e:
        await update.message.reply_text(f"Duh error pas nyimpen: {e}")

# --- HANDLING CHAT BIASA (Mikir pake Groq) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_user = update.message.text
    print(f"📩 Chat Masuk: {msg_user}")
    
    # Ambil konteks dari database dikit (Optional: Biar dia inget materi terakhir)
    # Untuk sekarang kita fokus biar dia gak crash dulu
    try:
        # Panggil AI Groq
        jawab = tanya_groq(msg_user)
        await update.message.reply_text(jawab, parse_mode="Markdown")
    except Exception as e:
        print(f"⚠️ Error di brain: {e}")
        await update.message.reply_text("Aduh, otak gue lagi nge-hang dikit, Cok!")

# --- MESIN UTAMA ---
if __name__ == '__main__':
    # Pastikan database siap dulu
    init_db()
    
    print(f"🚀 AGENT NGANJUK AKTIF! [{dapet_waktu_sekarang()}]")
    
    # Bangun aplikasi Telegram
    app = ApplicationBuilder().token(TOKEN_TELE).build()

    # Daftarin perintah
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Halo Cok! Agent Nganjuk siap bantu trading & coding lu!")))
    app.add_handler(CommandHandler("belajar", belajar))
    
    # Daftarin handler buat chat biasa
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Gas Pol!
    app.run_polling(drop_pending_updates=True)
        
