import os
import google.generativeai as genai

# Ambil API Key Gemini dari Railway
GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Pake model Flash biar responnya kilat buat scalping
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Upload foto ke AI
        sample_file = genai.upload_file(path=image_path, display_name="Chart Scalping")
        
        # Prompt khusus buat Trading (SMC/ICT Style)
        prompt = (
            "Lu adalah Master Trader SMC dan ICT. Analisa chart ini buat scalping XAUUSD. "
            "Cari area Order Block, Liquidity Sweep, FVG, atau ChoCh. "
            "Kasih tau gue: 1. Trend sekarang, 2. Area Entry, 3. SL & TP simpel. "
            "Jawab pake gaya bahasa santai kayak temen nongkrong di Nganjuk, pake 'Gue/Lu' dan 'Cok'."
        )
        
        response = model.generate_content([prompt, sample_file])
        return response.text
    except Exception as e:
        return f"Duh, mata gue lagi siwer, Cok! Gak bisa baca chart. Error: {e}"
      
