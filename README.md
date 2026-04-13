# GBC Analytics Dashboard

**Тестовое задание — AI Tools Specialist**

## Результат

- **Дашборд (Vercel)**: [https://project-3yfco-3ouaqrc7j-dzharmakhan-4402s-projects.vercel.app/](https://project-3yfco-3ouaqrc7j-dzharmakhan-4402s-projects.vercel.app/)
- **GitHub**: https://github.com/dzharmakhan-1/gbc-dashboard
- **Telegram бот**: @boboli_bot (уведомления при заказах > 50 000 ₸)

## Что сделано

- Загружены 50 тестовых заказов в RetailCRM через API
- Настроена синхронизация RetailCRM → Supabase
- Создан дашборд на Next.js 16 с графиком и статистикой
- Реализована система уведомлений в Telegram

## Структура проекта

- `app/` — Next.js дашборд
- `scripts/` — Python скрипты
  - `upload_to_crm.py` — загрузка заказов в RetailCRM
  - `sync_to_supabase.py` — синхронизация в Supabase
  - `telegram_notifications.py` — уведомления в Telegram

## Настройка окружения

1. Скопируйте файл `.env.example` в `.env`
2. Заполните реальными ключами

## Как запустить уведомления

```bash
cd scripts
python telegram_notifications.py
```

## Промпты, которые использовал (Codex)

1. **Загрузка заказов**:
   "Напиши Python-скрипт для загрузки массива заказов из mock_orders.json в RetailCRM API v5/orders/upload с правильным форматом items и totalSumm"

2. **Синхронизация**:
   "Сделай скрипт, который забирает заказы из RetailCRM и сохраняет их в Supabase через REST API (без тяжёлого клиента)"

3. **Дашборд**:
   "Создай чистый Next.js 16 дашборд с Chart.js, статистикой (выручка, средний чек) и графиком заказов из Supabase"

## Где застрял и как решил

- **Ошибка 460** (`orderType does not exist`) → удалил поле `orderType` из заказов
- **Проблемы с установкой `supabase` пакета** на Windows → перешёл на чистый `urllib` + REST API
- **Не нашёл раздел Webhooks** в RetailCRM → сделал отдельный мониторинговый скрипт `telegram_notifications.py`
- **404 на Vercel** → исправил Framework Preset на Next.js + улучшил обработку ошибок
- **Python/pip проблемы** → использовал встроенные модули

Всё тестовое задание выполнено с помощью Codex.

## Технологии

- RetailCRM API v5
- Supabase (Postgres + REST)
- Next.js 16 (App Router) + TypeScript + Tailwind
- Chart.js + react-chartjs-2
- Vercel

Готов к обсуждению и дальнейшим задачам!
