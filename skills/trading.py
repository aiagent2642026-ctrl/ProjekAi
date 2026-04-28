import random

def analisa_market(simbol):
    # Nanti di sini kita pasang API harga real-time
    # Sekarang kita bikin simulasi logika SMC/ICT dulu
    bias = random.choice(["BULLISH", "BEARISH", "SIDEWAYS"])
    ob_area = random.randint(2300, 2350)
    
    hasil = f"--- ANALISA {simbol.upper()} ---\n"
    hasil += f"Bias Hari Ini: {bias}\n"
    hasil += f"Area Order Block (H4): {ob_area}\n"
    hasil += "Saran: Tunggu Liquidity Sweep sebelum entry, tod!"
    
    return hasil

