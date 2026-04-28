import os
import base64
from groq import Groq

# Pastikan API Key Groq lu udah ada di Railway Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analisa_chart_vision(image_path):
    try:
        # Ubah gambar jadi base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Panggil Llama 3.2 Vision (Model terbaru & tercepat di Groq)
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Lu adalah Master Trader SMC/ICT dari Nganjuk. Analisa chart XAUUSD ini. Cari Order Block, FVG, atau Liquidity. Kasih saran entry, SL, dan TP. Jawab santai pake bahasa gue-lu dan cok!"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Duh, mata gue makin siwer, Cok! Gagal baca gambar. Error: {e}"
