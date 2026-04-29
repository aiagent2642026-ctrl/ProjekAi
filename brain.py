# brain.py
import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

def validasi_dan_arsiteki(raw_analysis):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    system_prompt = (
        "You are Lyria-Brain. Your job is to audit the vision analysis. "
        "Apply the 4-D Framework. If the vision analysis suggests a 'Buy' but HTF is Bearish, "
        "warn the user about an 'SMC Trap'. Ensure technical accuracy. "
        "Format the output to be clean for Telegram. Style: Nganjuk Casual."
    )
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Audit analisa ini, Cok: {raw_analysis}"}
        ]
    }
    
    res = requests.post(url, json=payload, headers=headers)
    return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else "Groq Error!"
