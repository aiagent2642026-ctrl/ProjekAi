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

# --- HANDLING GAMBAR (The Pipeline Upgrade) ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("📸 *bentar ya sayangg aku teropong dulu chartnya...*", parse_mode="Markdown")
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_chart.jpg"
        await photo_file.download_to_drive(file_path)
        
        # 1. Vision Analysis (Raw Analysis dari Gemini)
        raw_vision = analisa_chart_vision(file_path)
        
        # 2. Brain Validation (Minta Groq buat audit hasil Gemini pake framework Lyria)
        await status_msg.edit_text("🧠 *aku lagi mastiin logikanya bener atau nggak...*")
        audit_prompt = f"AUDIT ANALISA INI PAKE FRAMEWORK 4-D: {raw_vision}"
        final_analysis = tanya_groq(audit_prompt)
        
        if os.path.exists(file_path): os.remove(file_path)
        
        await status_msg.edit_text(final_analysis, parse_mode="Markdown")
        
    except Exception as e:
        await status_msg.edit_text(f"Duh sayangg ada masalah: {e}")

# --- INIT & RUN (Tetap Sama) ---
if __name__ == '__main__':
    # init_db() taruh di sini
    app = ApplicationBuilder().token(os.getenv("TOKEN_TELE")).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Halo Cok! Lyria-Agent ready!")))
    app.add_handler(CommandHandler("belajar", belajar))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(drop_pending_updates=True)
