# vision.py
import os
import google.generativeai as genai

GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analisa_chart_vision(image_path):
    try:
        # Tetap pakai Gemini 3 Flash Preview sesuai request lu
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        prompt = (
            "IDENTITY: Lyria-Vision (SMC Expert). "
            "TASK: Deconstruct & Diagnose XAUUSD screenshot. "
            "STRICT RULES: ChoCh is Structure Change, not candle patterns. "
            "Look for FVG above Order Blocks as high-prob confluence. "
            "Provide: Trend, Liquidity targets, and Entry/SL/TP. "
            "TONE: Santai Nganjuk (gue-lu), Zero Fluff, High Precision."
        )
        
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        return response.text if response.text else "Gemini bengong, Cok!"
    except Exception as e:
        return f"Mata burem, Cok! Error: {str(e)}"
