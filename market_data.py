import requests
import os

FINNHUB_KEY = os.getenv("FINNHUB_KEY")
FMP_KEY = os.getenv("FMP_KEY")

def get_live_gold_price():
    # Narik harga Gold (XAU/USD) real-time
    url = f"https://financialmodelingprep.com/api/v3/quote/XAUUSD?apikey={FMP_KEY}"
    try:
        response = requests.get(url).json()
        return response[0]['price'] if response else "Gagal narik harga"
    except:
        return "Server harga lagi maintenance, Cok!"

def get_high_impact_news():
    # Narik berita ekonomi hari ini
    url = f"https://finnhub.io/api/v1/calendar/economic?token={FINNHUB_KEY}"
    try:
        events = requests.get(url).json()['economicCalendar']
        # Filter yang dampaknya High aja
        high_impact = [f"{e['event']} ({e['country']})" for e in events if e['impact'] == 'high']
        return ", ".join(high_impact) if high_impact else "Gak ada berita ngeri hari ini."
    except:
        return "Gagal cek kalender, mending pantau ForexFactory aja!"
