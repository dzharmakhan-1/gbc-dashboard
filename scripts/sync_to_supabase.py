import json
import requests
import time

SUBDOMAIN = "dzharmakhan.retailcrm.ru"
API_KEY = "NaPHNvtKovilTjQ9LXJAKHjxY9PRhTzS"

SUPABASE_URL = "https://zwhhqkrghrlsmnmhmcbr.supabase.co"
SUPABASE_KEY = "sb_publishable_Pw1j1BQHsKEM7SerlP7bPg_ksRS0G0h"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"   # это включает upsert
}

print("🚀 Синхронизация RetailCRM → Supabase (простая версия без тяжёлых зависимостей)\n")

page = 1
limit = 100
total_synced = 0

while True:
    params = {
        "apiKey": API_KEY,
        "limit": limit,
        "page": page,
        "embed": "items,delivery"
    }

    try:
        response = requests.get(f"https://{SUBDOMAIN}/api/v5/orders", params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"Ошибка RetailCRM: {response.status_code}")
            print(response.text[:400])
            break

        data = response.json()
        orders = data.get("orders", [])

        if not orders:
            print("Все заказы обработаны.")
            break

        print(f"Страница {page}: получено {len(orders)} заказов")

        for order in orders:
            delivery = order.get("delivery") or {}
            address = delivery.get("address") or {}

            record = {
                "external_id": order.get("externalId"),
                "number": order.get("number"),
                "created_at": order.get("createdAt"),
                "total_summ": float(order.get("totalSumm") or 0),
                "status": order.get("status", {}).get("code") if isinstance(order.get("status"), dict) else str(order.get("status", "")),
                "first_name": order.get("firstName"),
                "last_name": order.get("lastName"),
                "phone": order.get("phone"),
                "email": order.get("email"),
                "city": address.get("city"),
                "raw_data": order
            }

            # Upsert в Supabase
            r = requests.post(
                f"{SUPABASE_URL}/rest/v1/orders",
                headers=headers,
                json=record
            )

            if r.status_code in (200, 201):
                total_synced += 1
            else:
                print(f"⚠️  Ошибка при сохранении заказа {order.get('number')}: {r.status_code} {r.text[:150]}")

        page += 1
        time.sleep(0.7)  # пауза, чтобы не превысить лимиты

    except Exception as e:
        print(f"Ошибка на странице {page}: {e}")
        break

print("\n" + "="*70)
print(f"Синхронизация завершена!")
print(f"Всего обработано заказов: {total_synced}")