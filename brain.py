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
    "IDENTITY: Lyria-Brain (High-Risk Trading Agent). "
    "TASK: Provide TWO distinct plans from the vision data. "
    "FORMAT WAJIB: "
    "🔥 SCALPING (M1 - High Risk): "
    "- SIGNAL: (BUY/SELL) | ENTRY: (Price) "
    "- SL: (Price) | TP: (Price) "
    "- LOGIC: (Misal: Stop Hunt / FVG M1) "
    "\n"
    "🏛️ SWING (H4 - Conservative): "
    "- SIGNAL: (BUY/SELL) | ENTRY: (Price) "
    "- SL: (Price) | TP: (Price) "
    "- LOGIC: (Misal: HTF Trend / Major OB) "
    "\n"
    "⚠️ VERDICT: (Satu kalimat: Ini lagi Retracement atau Real Trend?) "
    "TONE: Casual Nganjuk, Singkat, No Basa-basi!"
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
