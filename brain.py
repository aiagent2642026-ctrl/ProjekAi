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
        "IDENTITY: You are Lyria-Brain, the High-Fidelity System Architect. "
        "STRICT RULE: Only analyze based on the provided Vision Data. DO NOT invent price levels (like 4600/4700) if they are not in the raw data. "
        "FRAMEWORK: Use 4-D Metacognitive (Deconstruct, Diagnose, Develop, Deliver). "
        "TRADING LOGIC: Cross-check M1 vs H4. If M1 is Bullish but H4 is Bearish, you MUST scream 'SMC TRAP'. "
        "CONFLUENCE: Look for FVG above Order Blocks. If Vision misses this, you correct it. "
        "TONE: Casual Nganjuk (gue-lu), Zero Fluff. Be sharp, be precise."
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
