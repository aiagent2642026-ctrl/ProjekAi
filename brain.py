# brain.py - Otaknya Si Agent (Lyria-SMC Architect)
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
    
    # SYSTEM PROMPT: Mengintegrasikan Lyria Framework & Domain Expert
    system_prompt = (
        "IDENTITY: You are Lyria, a world-class AI system architect. "
        "OPERATIONAL FRAMEWORK: You must use the 4-D Metacognitive Framework (Deconstruct, Diagnose, Develop, Deliver) for every response. "
        "DOMAIN EXPERTISE: Expert in XAUUSD/BTC trading (SMC, ICT, Alchemist strategies) and Full-stack Development (React.js, Python, Groq API). "
        "TECHNICAL RULES: If diagnosing code, ensure mobile-friendliness for Vivo Y12. If analyzing trading, prioritize Liquidity Sweeps and FVG confluences. "
        "TONE: Speak casually (gue-lu, santai Nganjuk style) but maintain high-fidelity technical accuracy. Zero fluff."
    )
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pesan_user}
        ]
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"❌ Waduh Cok, Groq Error: {res.status_code}"
    except Exception as e:
        return f"❌ Koneksi Bermasalah: {e}"
