import requests
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

SUBDOMAIN = os.getenv("RETAILCRM_SUBDOMAIN")
API_KEY = os.getenv("RETAILCRM_API_KEY")

SUPABASE_URL = "https://zwhhqkrghrlsmnmhmcbr.supabase.co"
SUPABASE_KEY = "твой_service_role_key"   # ← замени на service_role ключ

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

print("🚀 Запуск синхронизации RetailCRM → Supabase...\n")

page = 1
total = 0

while True:
    params = {
        "apiKey": API_KEY,
        "limit": 100,
        "page": page,
        "embed": "items,delivery"
    }

    resp = requests.get(f"https://{SUBDOMAIN}.retailcrm.ru/api/v5/orders", params=params)
    data = resp.json()
    orders = data.get("orders", [])

    if not orders:
        break

    print(f"Страница {page}: {len(orders)} заказов")

    for order in orders:
        delivery = order.get("delivery") or {}
        address = delivery.get("address") or {}

        record = {
            "external_id": order.get("externalId"),
            "number": order.get("number"),
            "created_at": order.get("createdAt"),
            "total_summ": order.get("totalSumm"),
            "status": order.get("status", {}).get("code") if isinstance(order.get("status"), dict) else order.get("status"),
            "first_name": order.get("firstName"),
            "last_name": order.get("lastName"),
            "phone": order.get("phone"),
            "email": order.get("email"),
            "city": address.get("city"),
            "raw_data": order
        }

        r = requests.post(f"{SUPABASE_URL}/rest/v1/orders", headers=headers, json=record)
        if r.status_code in (200, 201):
            total += 1

    page += 1
    time.sleep(0.7)

print(f"\n✅ Синхронизация завершена. Обработано заказов: {total}")
