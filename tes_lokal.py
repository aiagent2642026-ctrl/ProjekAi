import sys
import os

# Biar folder hooks & skills kebaca
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hooks.trigger import proses_sebelum_chat

def tes_bot_offline():
    print("🤖 --- MODE SIMULASI OFFLINE (HEMAT KUOTA) ---")
    print("Ketik 'keluar' buat udahan.\n")
    
    while True:
        msg_user = input("Lu (Simulasi): ")
        
        if msg_user.lower() == 'keluar':
            break
            
        # Tes apakah Hook jalan
        print("\n[INFO] Mengecek Saraf (Hooks)...")
        pesan_akhir = proses_sebelum_chat(msg_user)
        
        if "[SYSTEM HOOK]" in pesan_akhir:
            print("✅ HOOK BERHASIL!")
            print(f"Isi Pesan yang bakal dikirim ke AI:\n\n{pesan_akhir}\n")
        else:
            print("ℹ️ Hook diem aja (gak ada keyword 'gold').")
            print(f"Pesan normal: {pesan_akhir}\n")

if __name__ == "__main__":
    tes_bot_offline()

