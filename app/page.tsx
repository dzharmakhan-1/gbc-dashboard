'use client';

import { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  useEffect(() => {
    if (!supabaseUrl || !supabaseKey) {
      setError('Environment variables NEXT_PUBLIC_SUPABASE_URL или NEXT_PUBLIC_SUPABASE_ANON_KEY не настроены в Vercel');
      setLoading(false);
      return;
    }

    async function fetchOrders() {
      try {
        const res = await fetch(
          `${supabaseUrl}/rest/v1/orders?select=*&order=created_at.desc&limit=100`,
          {
            method: 'GET',
            headers: {
              apikey: supabaseKey,
              Authorization: `Bearer ${supabaseKey}`,
              'Content-Type': 'application/json',
            } as HeadersInit,   // ← это фиксит TypeScript ошибку
          }
        );

        if (!res.ok) {
          throw new Error(`Supabase error: ${res.status} ${res.statusText}`);
        }

        const data = await res.json();
        setOrders(Array.isArray(data) ? data : []);
      } catch (err: any) {
        console.error('Fetch error:', err);
        setError(err.message || 'Не удалось загрузить данные из Supabase');
      } finally {
        setLoading(false);
      }
    }

    fetchOrders();
  }, [supabaseUrl, supabaseKey]);

  const totalOrders = orders.length;
  const totalRevenue = orders.reduce((sum, o) => sum + (Number(o.total_summ) || 0), 0);
  const avgCheck = totalOrders > 0 ? Math.round(totalRevenue / totalOrders) : 0;

  const chartData = {
    labels: orders.slice(0, 30).map((o) =>
      new Date(o.created_at).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
    ),
    datasets: [
      {
        label: 'Сумма заказов (₸)',
        data: orders.slice(0, 30).map((o) => Number(o.total_summ) || 0),
        borderColor: '#22c55e',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
        borderWidth: 3,
      },
    ],
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-xl">Загрузка дашборда...</div>;

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
        <div className="max-w-md text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Ошибка загрузки</h2>
          <p className="text-gray-700 mb-6">{error}</p>
          <p className="text-sm text-gray-500">Убедись, что добавил Environment Variables в Vercel и сделал Redeploy</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-10">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">📊 GBC Analytics Dashboard</h1>
        <p className="text-gray-600 mb-8">Заказы из RetailCRM • Данные из Supabase</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-3xl p-8 shadow">
            <p className="text-gray-500">Всего заказов</p>
            <p className="text-5xl font-semibold mt-3">{totalOrders}</p>
          </div>
          <div className="bg-white rounded-3xl p-8 shadow">
            <p className="text-gray-500">Общая выручка</p>
            <p className="text-5xl font-semibold mt-3">{totalRevenue.toLocaleString('ru-RU')} ₸</p>
          </div>
          <div className="bg-white rounded-3xl p-8 shadow">
            <p className="text-gray-500">Средний чек</p>
            <p className="text-5xl font-semibold mt-3">{avgCheck.toLocaleString('ru-RU')} ₸</p>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-8 shadow h-[480px]">
          <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
        </div>

        <p className="text-center text-sm text-gray-500 mt-10">
          50 тестовых заказов • Обновлено: {new Date().toLocaleString('ru-RU')}
        </p>
      </div>
    </div>
  );
}