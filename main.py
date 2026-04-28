import requests
import time
import sys
import os

# Biar Python tau folder kita ada di mana
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Panggil semua mesin dari file lain
import os
TOKEN_TELE = os.getenv("TOKEN_TELE")
# Lu juga bisa tambahin ini kalau butuh CHAT_ID
CHAT_ID = os.getenv("CHAT_ID") 
from brain import tanya_groq
from tools import dapet_waktu_sekarang

def kirim_tele(pesan):
    url = f"https://api.telegram.org/bot{TOKEN_TELE}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def jalankan_bot():
    print(f"🚀 AGENT NGANJUK AKTIF! [{dapet_waktu_sekarang()}]")
    # Bersihin pesan lama biar gak spam pas start
    requests.get(f"https://api.telegram.org/bot{TOKEN_TELE}/deleteWebhook?drop_pending_updates=True")

    offset = -1
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN_TELE}/getUpdates"
            r = requests.get(url, params={"offset": offset, "timeout": 15}).json()

            if r.get("ok") and r.get("result"):
                for up in r["result"]:
                    offset = up["update_id"] + 1
                    if "message" in up and "text" in up["message"]:
                        msg_user = up["message"]["text"]
                        print(f"📩 Chat: {msg_user}")

                        # --- BAGIAN HOOKS (Saraf Otomatis) ---
                        from hooks.trigger import proses_sebelum_chat
                        msg_user = proses_sebelum_chat(msg_user)

                        # AI Mikir pake brain.py
                        jawab = tanya_groq(msg_user)

                        # Kirim balik ke Tele
                        kirim_tele(f"🤖 *Agent:* {jawab}")
        except KeyboardInterrupt:
            print("\n❌ Bot dimatikan Ilham.")
            break
        except Exception as e:
            print(f"⚠️ Ada error dikit: {e}")
            time.sleep(2)

if __name__ == "__main__":
    jalankan_bot()

