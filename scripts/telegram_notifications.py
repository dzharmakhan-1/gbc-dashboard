import urllib.request
import urllib.parse
import json
import time

# ==================== НАСТРОЙКИ ====================
RETAILCRM_SUBDOMAIN = "dzharmakhan"
RETAILCRM_API_KEY = "NaPHNvtKovilTjQ9LXJAKHjxY9PRhTzS"

BOT_TOKEN = "8605419608:AAF6OJMNaSBR-c2P_zLWVf6PWJZiH0xRcnk"
CHAT_ID = "6388129213"

# Запоминаем уже обработанные заказы (чтобы не спамило)
processed_orders = set()

print("🚀 Скрипт уведомлений запущен (версия без спама)...\n")

while True:
    try:
        url = f"https://{RETAILCRM_SUBDOMAIN}.retailcrm.ru/api/v5/orders"
        params = {
            "apiKey": RETAILCRM_API_KEY,
            "limit": 50,
            "order": "desc"
        }
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))

        orders = data.get("orders", [])

        for order in orders:
            external_id = order.get("externalId") or order.get("id")
            total = float(order.get("totalSumm", 0))
            
            # Проверяем, не отправляли ли уже уведомление по этому заказу
            if external_id and external_id not in processed_orders and total > 50000:
                message = f"""🚨 <b>Большой заказ!</b>

№ {order.get('number', '—')}
Сумма: <b>{total:,.0f} ₸</b>
Клиент: {order.get('firstName', '')} {order.get('lastName', '')}
Телефон: {order.get('phone', '—')}
Дата: {order.get('createdAt', '—')}
"""

                # Отправка
                try:
                    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    data_send = urllib.parse.urlencode({
                        "chat_id": CHAT_ID,
                        "text": message,
                        "parse_mode": "HTML"
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(send_url, data=data_send, method='POST')
                    with urllib.request.urlopen(req):
                        pass
                    
                    print(f"✅ Уведомление отправлено → Заказ №{order.get('number')} на {total} ₸")
                    processed_orders.add(external_id)
                    
                except Exception as e:
                    print(f"Ошибка отправки: {e}")

    except Exception as e:
        print(f"Ошибка проверки: {e}")

    time.sleep(20)