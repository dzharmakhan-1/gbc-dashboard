import json
import requests
import uuid
import time
from dotenv import load_dotenv
import os

load_dotenv()

SUBDOMAIN = os.getenv("RETAILCRM_SUBDOMAIN")
API_KEY = os.getenv("RETAILCRM_API_KEY")
SITE_CODE = "mysklad"   # или "main", если не работает

url = f"https://{SUBDOMAIN}.retailcrm.ru/api/v5/orders/upload"

with open('mock_orders.json', 'r', encoding='utf-8') as f:
    orders = json.load(f)

print(f"Загружено {len(orders)} заказов\n")

for i, order in enumerate(orders, 1):
    order["externalId"] = str(uuid.uuid4())[:12]
    
    if "orderType" in order:
        del order["orderType"]
    
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

    order["totalSumm"] = round(sum(
        item.get("initialPrice", 0) * item.get("quantity", 1) 
        for item in order.get("items", [])
    ), 2)

    payload = {
        "site": SITE_CODE,
        "orders": json.dumps([order], ensure_ascii=False)
    }

    response = requests.post(url, params={"apiKey": API_KEY}, data=payload)
    
    print(f"Order {i:2d}/{len(orders)} → {response.status_code} {'✅' if response.status_code == 201 else '❌'}")
    
    if i % 10 == 0:
        time.sleep(1)

print("\nЗагрузка завершена!")
