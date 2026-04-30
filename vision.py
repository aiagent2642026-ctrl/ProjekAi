# vision.py
import os
import google.generativeai as genai

GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Pake model flash buat vision yang cepet
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if not os.path.exists(image_path):
            return "File fotonya gak ketemu, Cok!"

        with open(image_path, "rb") as f:
            image_data = f.read()

        # SEKARANG SUDAH MENJOROK KE DALEM (LURUS):
        prompt = (
            "Sebutkan HANYA data mentah berikut dari gambar: "
            "1. Harga running saat ini. "
            "2. Trend visual (Bullish/Bearish). "
            "3. Lokasi FVG atau OB (angka saja). "
            "DILARANG KERAS membuat format Scalping/Swing atau memberi sinyal Entry/SL/TP. "
            "Berikan data dalam bentuk poin-poin singkat saja."
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
