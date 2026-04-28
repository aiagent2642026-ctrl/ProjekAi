import os
import google.generativeai as genai

# Pastikan di Railway lu udah ada variabel: GEMINI_KEY
GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Pake model flash, ini stabil dan jago baca chart trading
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Baca file gambarnya
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        # Prompt sakti buat scalping
        prompt = (
            "Lu adalah Suhu Trading SMC/ICT dari Nganjuk. Analisa screenshot chart XAUUSD ini. "
            "Cari area Order Block, FVG, atau Liquidity yang mantap. "
            "Saranin Entry, SL, dan TP buat scalping. Jawab santai pake bahasa gue-lu dan cok!"
        )
        
        # Eksekusi kirim ke Google
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        return response.text
    except Exception as e:
        return f"Duh, mata gue makin siwer, Cok! Gagal baca gambar. Error: {e}"
