import urllib.request
import urllib.parse
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

RETAILCRM_SUBDOMAIN = os.getenv("RETAILCRM_SUBDOMAIN")
RETAILCRM_API_KEY = os.getenv("RETAILCRM_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

processed_orders = set()

print("🚀 Скрипт уведомлений запущен (без спама)...\n")

while True:
    try:
        url = f"https://{RETAILCRM_SUBDOMAIN}.retailcrm.ru/api/v5/orders"
        params = {"apiKey": RETAILCRM_API_KEY, "limit": 50, "order": "desc"}
        
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(full_url) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        for order in data.get("orders", []):
            ext_id = order.get("externalId") or order.get("id")
            total = float(order.get("totalSumm", 0))

            if ext_id and ext_id not in processed_orders and total > 50000:
                message = f"""🚨 <b>Большой заказ!</b>

№ {order.get('number', '—')}
Сумма: <b>{total:,.0f} ₸</b>
Клиент: {order.get('firstName', '')} {order.get('lastName', '')}
Телефон: {order.get('phone', '—')}
"""

                send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data_send = urllib.parse.urlencode({
                    "chat_id": CHAT_ID,
                    "text": message,
                    "parse_mode": "HTML"
                }).encode('utf-8')

                req = urllib.request.Request(send_url, data=data_send, method='POST')
                with urllib.request.urlopen(req):
                    pass

                print(f"✅ Уведомление → Заказ №{order.get('number')} ({total} ₸)")
                processed_orders.add(ext_id)

    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(20)
