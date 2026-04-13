import json
import requests
import uuid
import time
from datetime import datetime

# ==================== ТВОИ ДАННЫЕ ====================
SUBDOMAIN = "dzharmakhan.retailcrm.ru"
API_KEY = "NaPHNvtKovilTjQ9LXJAKHjxY9PRhTzS"
SITE_CODE = "dzharmakhan"          # попробуй также "main" или "default", если не сработает

url = f"https://{SUBDOMAIN}/api/v5/orders/upload"

with open('mock_orders.json', 'r', encoding='utf-8') as f:
    orders = json.load(f)

print(f"✅ Загружено {len(orders)} заказов из mock_orders.json\n")
print(f"URL: {url}")
print(f"Site code: {SITE_CODE}\n")

success_count = 0
error_count = 0
log_file = "upload_errors.log"

with open(log_file, "w", encoding="utf-8") as log:
    log.write(f"Upload started at {datetime.now()}\n\n")

for i, order in enumerate(orders, 1):
    original_order = order.copy()  # для лога в случае ошибки
    
    # Основные исправления
    order["externalId"] = str(uuid.uuid4())[:12]
    
    # УДАЛЯЕМ проблемное поле — это главное решение
    if "orderType" in order:
        del order["orderType"]
    
    # Альтернатива: можно попробовать задать существующий тип
    # order["orderType"] = "eshop"   # раскомментируй, если хочешь
    
    # Исправляем items
    if isinstance(order.get("items"), list):
        order["items"] = [
            {
                "productName": item.get("productName", "Товар"),
                "quantity": int(item.get("quantity", 1)),
                "initialPrice": float(item.get("initialPrice", 0)),
                "offer": {"name": item.get("productName", "Товар")}
            } for item in order["items"]
        ]
    else:
        order["items"] = []

    # totalSumm
    order["totalSumm"] = round(sum(
        item.get("initialPrice", 0) * item.get("quantity", 1) 
        for item in order.get("items", [])
    ), 2)

    payload = {
        "site": SITE_CODE,
        "orders": json.dumps([order], ensure_ascii=False)
    }

    try:
        response = requests.post(
            url,
            params={"apiKey": API_KEY},
            data=payload,
            timeout=30
        )

        print(f"Order {i:2d}/{len(orders)} → Status: {response.status_code} ", end="")

        if response.status_code == 201:
            success_count += 1
            print("✅ Успешно загружен")
        else:
            error_count += 1
            print("❌ Ошибка")
            try:
                error_data = response.json()
                error_msg = error_data.get("errorMsg", response.text[:200])
                print(f"   → {error_msg}")
                
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"Order {i} | externalId: {order['externalId']} | Error: {error_msg}\n")
            except:
                print(f"   → {response.text[:300]}")
                
    except Exception as e:
        error_count += 1
        print(f"Order {i} → Исключение: {e}")
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Order {i} | Exception: {e}\n")

    if i % 10 == 0:
        time.sleep(0.8)  # небольшая пауза

print("\n" + "="*60)
print(f"🎉 ЗАВЕРШЕНО!")
print(f"✅ Успешно загружено: {success_count}")
print(f"❌ Ошибок: {error_count}")
print(f"📄 Лог ошибок сохранён в файл: {log_file}")

if success_count > 0:
    print("\nТеперь зайди в RetailCRM → раздел «Заказы» и проверь, появились ли заказы.")
