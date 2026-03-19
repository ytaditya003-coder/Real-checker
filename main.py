import requests
from bs4 import BeautifulSoup
import time
import os
import random

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PRODUCT_URLS_STR = os.getenv('PRODUCT_URLS')

def check_stock(url):
    # Alag-alag User-Agents taaki block na ho
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 403:
            print("🚨 Alert: SHEIN ne temporary block kiya hai. Waiting longer...")
            return "blocked"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text().lower()
        
        # Stock check logic
        if ("add to bag" in content or "add to cart" in content) and ("sold out" not in content):
            return True
        return False
    except:
        return False

def send_msg(url):
    text = f"✅ **PRODUCT IN STOCK!**\n\nLink: {url}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

urls = [u.strip() for u in PRODUCT_URLS_STR.split(',')]
print(f"Bot Active! Monitoring {len(urls)} items.")

while True:
    random.shuffle(urls) # Links ka order badalte raho
    for url in urls:
        status = check_stock(url)
        if status == True:
            send_msg(url)
            time.sleep(10) 
        elif status == "blocked":
            time.sleep(600) # 10 min break agar block hue toh
            
        # Do products ke beech random gap (10-20 seconds)
        time.sleep(random.randint(10, 20))
    
    # Pura cycle khatam hone par 5 min ka lamba break (Risk kam karne ke liye)
    print("Cycle complete. Sleeping for 5 minutes...")
    time.sleep(300)
  
