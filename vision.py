import os
import google.generativeai as genai

# Ambil API Key dari Railway Variables
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Konfigurasi library
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
else:
    print("⚠️ WARNING: GEMINI_KEY belum diset di Variables Railway!")

def analisa_chart_vision(image_path):
    try:
        # Pake model flash, paling stabil dan jago baca chart trading
        # Kalau ini error 404, berarti project Google AI Studio lu belum aktif sempurna
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Baca file gambarnya
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        # Prompt sakti buat scalping ala Nganjuk Pride
        prompt = (
            "Lu adalah Suhu Trading SMC/ICT dari Nganjuk. Analisa screenshot chart XAUUSD ini. "
            "Cari area Order Block (OB), Fair Value Gap (FVG), atau Liquidity sweep yang mantap. "
            "Tentukan Trend utama dan structure market sekarang (BOS/ChoCh). "
            "Kasih saran Entry, SL, dan TP buat scalping cepat. Jawab santai pake bahasa gue-lu dan cok!"
        )
        
        # Eksekusi kirim ke Google pake format inline data
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        if response.text:
            return response.text
        else:
            return "Waduh Cok, Google-nya diem aja, gak ngasih analisa."
            
    except Exception as e:
        # Menampilkan error yang lebih jelas biar kita tau masalahnya
        return f"Duh, mata gue makin siwer, Cok! Gagal baca gambar. \n\nError: {str(e)}"
        
