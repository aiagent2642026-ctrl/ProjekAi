import os
import psycopg2
import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from vision import analisa_chart_vision # Panggil file baru tadi
from market_data import get_live_gold_price, get_high_impact_news

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
    msg_user = update.message.text.lower() # Kita bikin kecil semua hurufnya biar gak baperan
    print(f"📩 Chat Masuk: {msg_user}")
    
    try:
        # 1. AMBIL ILMU DARI DATABASE
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Kita pecah chat lu jadi kata-kata, trus cari yang paling relevan
        kata_kunci = msg_user.split()
        hasil_catatan = []
        
        for kata in kata_kunci:
            if len(kata) > 3: # Cari kata yang panjangnya lebih dari 3 huruf biar gak spam
                cur.execute("SELECT materi FROM brain_data WHERE materi ILIKE %s LIMIT 1", (f"%{kata}%",))
                row = cur.fetchone()
                if row:
                    hasil_catatan.append(row[0])
        
        cur.close()
        conn.close()

        # 2. PANGGIL OTAK AI (GROQ)
        jawab_ai = tanya_groq(msg_user)

        # 3. GABUNGIN JAWABAN (PAKSA DIA JAWAB PAKE INGATAN DULU)
        if hasil_catatan:
            # Ambil catatan pertama yang ketemu
            catatan_final = hasil_catatan[0]
            respon_final = f"📌 *INGATAN GUE:* {catatan_final}\n\n---\n🤖 *Analisa AI:* {jawab_ai}"
        else:
            respon_final = jawab_ai

        await update.message.reply_text(respon_final, parse_mode="Markdown")

    except Exception as e:
        print(f"⚠️ Error Database: {e}")
        jawab_ai = tanya_groq(msg_user)
        await update.message.reply_text(jawab_ai)

    # Ambil konteks dari database dikit (Optional: Biar dia inget materi terakhir)
    # Untuk sekarang kita fokus biar dia gak crash dulu
    try:
        # Panggil AI Groq
        jawab = tanya_groq(msg_user)
        await update.message.reply_text(jawab, parse_mode="Markdown")
    except Exception as e:
        print(f"⚠️ Error di brain: {e}")
        await update.message.reply_text("Aduh, otak gue lagi nge-hang dikit, Cok!")
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📸 *Sik Cok, gue teropong dulu chart lu...* 🔭", parse_mode="Markdown")
    
    try:
        # Download foto
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_chart.jpg"
        await photo_file.download_to_drive(file_path)
        
        # Analisa pake mata Gemini
        hasil_analisa = analisa_chart_vision(file_path)
        
        # Hapus file sampah
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await msg.edit_text(hasil_analisa)
    except Exception as e:
        await msg.edit_text(f"Gagal baca gambar, Cok! Error: {e}")
            
# --- MESIN UTAMA ---
if __name__ == '__main__':
    # Pastikan database siap dulu
    init_db()
    
    print(f"🚀 AGENT NGANJUK AKTIF! [{dapet_waktu_sekarang()}]")
    
    # Bangun aplikasi Telegram
    app = ApplicationBuilder().token(TOKEN_TELE).build()

    # Daftarin perintah
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Halo Cok! Agent Nganjuk siap bantu trading & coding lu!")))
    app.add_handler(CommandHandler("belajar", belajar))
    
    # Daftarin handler buat chat biasa
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Gas Pol!
    app.run_polling(drop_pending_updates=True)
        
