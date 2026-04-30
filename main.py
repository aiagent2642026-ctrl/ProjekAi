# main.py - The Orchestrator
import os, psycopg2, logging, sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from vision import analisa_chart_vision
from market_data import get_live_gold_price, get_high_impact_news
from brain import tanya_groq
from tools import dapet_waktu_sekarang

# --- KONEKSI DATABASE (Tetap Sama) ---
def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')

# --- HANDLING CHAT BIASA (Refined with Lyria Logic) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_user = update.message.text
    try:
        harga = get_live_gold_price()
        berita = get_high_impact_news()
        
        # Cari di Database (Memory Retrieval)
        conn = get_db_connection()
        cur = conn.cursor()
        kata_kunci = msg_user.lower().split()
        hasil_catatan = None
        for kata in (k for k in kata_kunci if len(k) > 3):
            cur.execute("SELECT materi FROM brain_data WHERE materi ILIKE %s LIMIT 1", (f"%{kata}%",))
            row = cur.fetchone()
            if row: 
                hasil_catatan = row[0]
                break
        cur.close()
        conn.close()

        # RAKIT PROMPT: Masukin catatan internal biar Groq nggak ngaco
        konteks_ingatan = f"Catatan Internal: {hasil_catatan}" if hasil_catatan else "Tidak ada catatan khusus."
        prompt_ai = (
            f"SYSTEM CONTEXT: {konteks_ingatan}\n"
            f"MARKET DATA: Harga {harga}, News {berita}\n"
            f"USER REQUEST: {msg_user}"
        )
        
        jawab_ai = tanya_groq(prompt_ai)
        
        # Gabungin Output biar tetep ada label Ingatan (Opsional)
        prefix = f"📌 *INGATAN GUE:* {hasil_catatan}\n\n---\n" if hasil_catatan else ""
        await update.message.reply_text(f"{prefix}{jawab_ai}", parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(tanya_groq(msg_user))

# --- HANDLING GAMBAR (The Pipeline Upgrade - FIXED) ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("📸 *bentar ya sayangg aku teropong dulu chartnya...*", parse_mode="Markdown")
    try:
        # 1. Download Foto
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_chart.jpg"
        await photo_file.download_to_drive(file_path)
        
        # 2. Vision Analysis (Raw Analysis dari Gemini)
        raw_vision = analisa_chart_vision(file_path)
        
        # 3. Brain Validation & Single Output Logic
        await status_msg.edit_text("🧠 *mikir keras biar gak double sinyal...*", parse_mode="Markdown")
        
        # Kita pertegas perintahnya di sini biar gak dobel-dobel
        perintah_final = (
            f"DARI DATA INI: {raw_vision}\n\n"
            "TOLONG BUATKAN HANYA 1 RESPON YANG TERDIRI DARI:\n"
            "1. SATU PLAN SCALPING (M1)\n"
            "2. SATU PLAN SWING (H4)\n"
            "DILARANG MEMBERIKAN LEBIH DARI ITU. GABUNGKAN JADI SATU KESIMPULAN."
        )
        
        final_analysis = tanya_groq(perintah_final)
        
        # Hapus file sampah
        if os.path.exists(file_path): 
            os.remove(file_path)
        
        # 4. Kirim hasil final
        await status_msg.edit_text(final_analysis, parse_mode="Markdown")
        
    except Exception as e:
        # Menangani error dengan rapi
        if 'status_msg' in locals():
            await status_msg.edit_text(f"Duh sayangg ada masalah: {e}")
        else:
            await update.message.reply_text(f"Duh sayangg ada masalah: {e}")
# --- FITUR /belajar (TARUH INI DI MAIN.PY) ---
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
        await update.message.reply_text("Oke, udah gue catat di otak!")
    except Exception as e:
        await update.message.reply_text(f"Duh error pas nyimpen: {e}")
        
# --- INIT & RUN (Tetap Sama) ---
if __name__ == '__main__':
    # init_db() taruh di sini
    app = ApplicationBuilder().token(os.getenv("TOKEN_TELE")).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Halo Cok! Lyria-Agent ready!")))
    app.add_handler(CommandHandler("belajar", belajar))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(drop_pending_updates=True)
