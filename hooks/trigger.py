import sys
import os

# Biar bisa manggil folder skills
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.trading import analisa_market

def proses_sebelum_chat(pesan_user):
    kata_kunci = ["gold", "xau", "analisa"]
    
    # Cek apakah user nanya soal trading
    if any(k in pesan_user.lower() for k in kata_kunci):
        data_trading = analisa_market("XAUUSD")
        return f"{pesan_user}\n\n[SYSTEM HOOK]:\n{data_trading}"
    
    return pesan_user

