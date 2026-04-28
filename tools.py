# tools.py - Kumpulan fungsi pembantu (Agent Tools)
import datetime

def hitung_lot(balance, risk_percent, pips):
    # Logika simpel hitung lot biar gak margin call
    risk_amount = balance * (risk_percent / 100)
    # Contoh standar: 1 lot = $10 per pip
    lot = risk_amount / (pips * 10)
    return round(lot, 2)

def dapet_waktu_sekarang():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Lu bisa nambahin fungsi scraping harga XAUUSD di sini nanti

