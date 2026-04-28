# brain.py - Otaknya Si Agent
import requests
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


def tanya_groq(pesan_user):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # System Prompt: Di sini lu bisa atur sifat AI lu
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system", 
                "content": "Kamu adalah Agent AI Nganjuk. Kamu ahli dalam Trading Gold (XAUUSD) dengan metode SMC/ICT dan jago coding Python. Jawab dengan gaya santai tapi cerdas."
            },
            {"role": "user", "content": pesan_user}
        ]
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"❌ Waduh, Groq Error: {res.status_code}"
    except Exception as e:
        return f"❌ Masalah Koneksi: {e}"

