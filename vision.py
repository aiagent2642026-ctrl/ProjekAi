import os
import google.generativeai as genai

# Ambil API Key dari Railway
GEMINI_KEY = os.getenv("GEMINI_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Panggil model Gemini 3 Flash Preview
        # Note: Nama model resminya biasanya 'gemini-3-flash-preview'
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        prompt = (
            "Lu adalah Master Trader SMC/ICT Nganjuk. Analisa screenshot chart XAUUSD ini pake model Gemini 3 Flash. "
            "Cari area Order Block, FVG, dan Liquidity sweep dengan sangat teliti. "
            "Tentukan Trend, BOS/ChoCh, dan kasih saran Entry, SL, TP buat scalping. "
            "Jawab santai pake bahasa gue-lu dan cok!"
        )
        
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        if response.text:
            return response.text
        else:
            return "Waduh Cok, si Gemini 3 diem aja, nggak ngasih analisa."
            
    except Exception as e:
        # Jika 'gemini-3-flash-preview' belum tersedia di region lu, 
        # dia bakal otomatis kasih tau errornya di sini.
        return f"Duh, mata Gemini 3 gue masih burem, Cok! \nError: {str(e)}"
