import os
import base64
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analisa_chart_vision(image_path):
    # Groq butuh gambar diubah jadi teks (base64)
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    try:
        completion = client.chat.completions.create(
            # Ganti baris modelnya jadi yang baru ini:
model="llama-3.2-11b-vision-preview"
            # Ini model Groq yang punya mata
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analisa chart XAUUSD ini pake teknik SMC/ICT. Cari Order Block atau FVG. Jawab gaya Nganjuk santai, Cok!"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}",
                            },
                        },
                    ],
                }
            ],
            temperature=0.5,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Duh, mata LLaVA gue burem, Cok! Error: {e}"
                    
