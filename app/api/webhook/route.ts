import { NextRequest } from 'next/server';

const BOT_TOKEN = '8605419608:AAF6OJMNaSBR-c2P_zLWVf6PWJZiH0xRcnk';
const CHAT_ID = '6388129213';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const order = body.order || body;

    // Проверяем сумму заказа
    const totalSumm = Number(order.totalSumm) || Number(order.total_summ) || 0;

    if (totalSumm > 50000) {
      const message = `🚨 Новый большой заказ!\n\n` +
        `№ ${order.number || '—'}\n` +
        `Сумма: ${totalSumm.toLocaleString('ru-RU')} ₸\n` +
        `Клиент: ${order.firstName || ''} ${order.lastName || ''}\n` +
        `Телефон: ${order.phone || '—'}`;

      await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: CHAT_ID,
          text: message,
          parse_mode: 'HTML'
        }),
      });

      console.log(`✅ Уведомление отправлено в Telegram. Сумма: ${totalSumm} ₸`);
    }

    return Response.json({ ok: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return Response.json({ ok: false }, { status: 500 });
  }
}