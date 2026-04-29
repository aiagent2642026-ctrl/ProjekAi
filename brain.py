# brain.py
import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

def tanya_groq(pesan_user):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # SYSTEM PROMPT BARU: Lebih Galak & Terpaku Data
    system_prompt = (
    "IDENTITY: Lyria-Brain (The Final Judge). "
    "TASK: Combine Vision data into ONE final decision. "
    "STRICT RULE: If M1 is Bullish but H4 is Bearish, you MUST call it a 'RETRACEMENT' or 'TRAP'. "
    "OUTPUT FORMAT (MUST BE THIS): "
    "1. STRUKTUR: (H4 vs M1 status) "
    "2. SIGNAL: (BUY/SELL/WAIT) "
    "3. ENTRY: (Price) | SL: (Price) | TP: (Price) "
    "4. REASON: (Max 2 lines, focus on FVG/OB). "
    "TONE: Singkat, Padat, No Basa-basi!"
)

    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pesan_user}
        ],
        "temperature": 0.2 # Diturunin biar dia gak 'ngarang' (lebih kaku tapi akurat)
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"❌ Groq Error: {res.status_code}"
    except Exception as e:
        return f"❌ Koneksi Masalah: {e}"
