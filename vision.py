# vision.py - Ahli Baca Chart (Lyria-Vision)
import os
import google.generativeai as genai

GEMINI_KEY = os.getenv("GEMINI_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Gunakan model terbaru yang tersedia
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        # PROMPT LOGIKA LYRIA: Presisi & Arsitektural
        prompt = (
            "IDENTITY: You are Lyria-Vision. Analyze this XAUUSD chart screenshot using the 4-D Framework. "
            "DECONSTRUCT: Identify Market Structure (HTF/LTF), Trend, and BOS/ChoCh. "
            "DIAGNOSE: Locate high-probability Order Blocks and Liquidity zones. "
            "CRITICAL CHECK: If there is an FVG (Fair Value Gap) above an Order Block, mark it as a STRONGER confirmation for Scalping. "
            "DEVELOP/DELIVER: Provide precise Entry, SL, and TP. "
            "TONE: Professional accuracy delivered in casual 'gue-lu' Nganjuk style. No unnecessary chatter."
        )
        
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        if response.text:
            return response.text
        else:
            return "Waduh Cok, si Gemini lagi merem, nggak ada teks analisanya."
            
    except Exception as e:
        return f"Duh, mata Gemini gue lagi burem, Cok! \nError: {str(e)}"
