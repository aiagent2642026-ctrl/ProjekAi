# vision.py
import os
import google.generativeai as genai

GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Pake model flash buat vision yang cepet
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        if not os.path.exists(image_path):
            return "File fotonya gak ketemu, Cok!"

        with open(image_path, "rb") as f:
            image_data = f.read()
            
        # PROMPT KHUSUS: Biar Gemini cuma lapor data mentah ke Groq
        prompt = (
            "Kamu adalah mata bagi AI trading. TUGAS UTAMA: "
            "1. Sebutkan angka harga (Running Price) yang tertera di chart. "
            "2. Identifikasi Trend (Bullish/Bearish) secara visual. "
            "3. Sebutkan angka koordinat FVG atau Order Block yang terlihat. "
            "DILARANG KERAS memberikan saran Entry, SL, atau TP! "
            "Cukup lapor data mentah agar diolah oleh tim eksekusi."
        )
        
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        if response and response.text:
            return response.text
        else:
            return "Gemini bengong, gak liat apa-apa, Cok!"
            
    except Exception as e:
        return f"Mata burem, Cok! Error: {str(e)}"
        
