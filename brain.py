# brain.py
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
    
    # SYSTEM PROMPT: Satu suara, gak pake debat
    system_prompt = (
        "IDENTITY: Lyria-Brain (The Final Judge). "
        "STRICT RULE: Dilarang keras mengulang atau copy-paste teks dari Vision! "
        "TASK: Ambil data harga dari Vision, buang analisanya, buat keputusan BARU yang konsisten. "
        "Hanya berikan SATU blok Scalping dan SATU blok Swing. "
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
        "\n⚠️ **VERDICT**: (TRAP atau TREND?)"
        "\n"
        "TONE: Singkat, Padat, Nganjuk Style."
    )

    # SEMUA BAGIAN DI BAWAH INI HARUS MENJOROK KE DALAM (INDENTED)
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pesan_user}
        ],
        "temperature": 0  # Biar robotnya kaku dan gak ngarang
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"❌ Groq Error: {res.status_code}"
    except Exception as e:
        return f"❌ Koneksi Masalah: {e}"
