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
    "STRICT RULE: Dilarang keras mengulang atau copy-paste teks dari Vision! "
    "TASK: Ambil data harga dari Vision, tapi buang analisanya. "
    "Buat keputusan BARU yang konsisten. "
    "\n"
    "FORMAT WAJIB (HANYA INI): "
    "\n🔥 **SCALPING (M1)**"
    "\n- SIGNAL: (BUY/SELL) | ENTRY: (Harga)"
    "\n- SL: (Harga) | TP: (Harga)"
    "\n- LOGIC: (1 kalimat)"
    "\n"
    "\n🏛️ **SWING (H4)**"
    "\n- SIGNAL: (BUY/SELL) | ENTRY: (Harga)"
    "\n- SL: (Harga) | TP: (Harga)"
    "\n- LOGIC: (1 kalimat)"
    "\n"
    "\n⚠️ **VERDICT**: (Pilih: TRAP atau TREND?)"
    "\n"
    "TONE: Singkat, Padat, Nganjuk Style."
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
