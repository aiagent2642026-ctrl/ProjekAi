import os
import psycopg2
import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from vision import analisa_chart_vision
from market_data import get_live_gold_price, get_high_impact_news

# Biar folder project kebaca
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load mesin dari file lu yang lain
from brain import tanya_groq
from tools import dapet_waktu_sekarang

# Ambil Variables dari Railway
TOKEN_TELE = os.getenv("TOKEN_TELE")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- KONEKSI DATABASE ---
def get_db_connection():
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
        await update.message.reply_text("Kasih materinya dong Cok! Contoh: /belajar Gold itu sideways.")
        return
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO brain_data (materi, kategori) VALUES (%s, %s)", (materi_baru, "umum"))
        conn.commit()
        cur.close()
        conn.close()
        await update.message.reply_text("iya sayangg")
    except Exception as e:
        await update.message.reply_text(f"Duh error pas nyimpen: {e}")

# --- HANDLING CHAT BIASA ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_user = update.message.text
    print(f"📩 Chat Masuk: {msg_user}")
    
    try:
        # 1. AMBIL DATA REAL-TIME & DATABASE
        harga = get_live_gold_price()
        berita = get_high_impact_news()
        
        # Cari di database (Ingatan)
        conn = get_db_connection()
        cur = conn.cursor()
        kata_kunci = msg_user.lower().split()
        hasil_catatan = []
        for kata in kata_kunci:
            if len(kata) > 3:
                cur.execute("SELECT materi FROM brain_data WHERE materi ILIKE %s LIMIT 1", (f"%{kata}%",))
                row = cur.fetchone()
                if row: hasil_catatan.append(row[0])
        cur.close()
        conn.close()

        # 2. RAKIT PROMPT & TANYA AI
        prompt_ai = f"INFO LIVE (Harga: {harga}, News: {berita}). Pertanyaan: {msg_user}"
        jawab_ai = tanya_groq(prompt_ai)

        # 3. GABUNGIN JAWABAN
        if hasil_catatan:
            respon_final = f"📌 *INGATAN GUE:* {hasil_catatan[0]}\n\n---\n🤖 *Analisa AI:* {jawab_ai}"
        else:
            respon_final = jawab_ai

        await update.message.reply_text(respon_final, parse_mode="Markdown")

    except Exception as e:
        print(f"⚠️ Error: {e}")
        # Fallback kalau database/api mati, tetep tanya Groq
        jawab_simple = tanya_groq(msg_user)
        await update.message.reply_text(jawab_simple)

# --- HANDLING GAMBAR ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📸 *bentar ya sayangg aku analisa dulu...*", parse_mode="Markdown")
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_chart.jpg"
        await photo_file.download_to_drive(file_path)
        
        hasil_analisa = analisa_chart_vision(file_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        await msg.edit_text(hasil_analisa)
    except Exception as e:
        await msg.edit_text(f"Gagal baca gambar, Cok! Error: {e}")

# --- MESIN UTAMA ---
if __name__ == '__main__':
    init_db()
    print(f"🚀 AGENT NGANJUK AKTIF! [{dapet_waktu_sekarang()}]")
    
    app = ApplicationBuilder().token(TOKEN_TELE).build()
    
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Halo Cok! Agent Nganjuk ready!")))
    app.add_handler(CommandHandler("belajar", belajar))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling(drop_pending_updates=True)
