import { AlertTriangle, DollarSign, Package, ShoppingCart, Users } from "lucide-react";
import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import MetricCard from "../components/MetricCard";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";
import api from "../services/api";
import { money } from "../utils/format";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get("/dashboard/summary").then((res) => setData(res.data));
  }, []);

  if (!data) return <div className="screen-center min-h-96">Loading analytics...</div>;

  return (
    <>
      <PageHeader title="Dashboard" description="Live operating metrics, recent orders, and inventory status." />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <MetricCard title="Products" value={data.total_products} icon={Package} />
        <MetricCard title="Customers" value={data.total_customers} icon={Users} tone="success" />
        <MetricCard title="Orders" value={data.total_orders} icon={ShoppingCart} />
        <MetricCard title="Revenue" value={money(data.total_revenue)} icon={DollarSign} tone="success" />
        <MetricCard title="Low stock" value={data.low_stock_products} icon={AlertTriangle} tone="warning" />
      </div>
      <div className="mt-5 grid gap-5 xl:grid-cols-[1.4fr_1fr]">
        <div className="panel p-4">
          <h2 className="mb-4 font-semibold text-ink">Monthly sales</h2>
          <div className="h-72">
            <ResponsiveContainer>
              <BarChart data={data.monthly_sales}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="panel p-4">
          <h2 className="mb-4 font-semibold text-ink">Inventory status</h2>
          <div className="h-72">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={data.inventory_status} dataKey="value" nameKey="label" outerRadius={92} label>
                  {["#0f766e", "#a15c07", "#b42318"].map((color) => <Cell key={color} fill={color} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <div className="mt-5 grid gap-5 xl:grid-cols-2">
        <div className="panel overflow-hidden">
          <h2 className="border-b border-line p-4 font-semibold text-ink">Recent orders</h2>
          <table className="table">
            <tbody className="divide-y divide-line">
              {data.recent_orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.order_number}</td>
                  <td><StatusBadge status={order.status} /></td>
                  <td className="text-right font-semibold">{money(order.total)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="panel overflow-hidden">
          <h2 className="border-b border-line p-4 font-semibold text-ink">Top selling products</h2>
          <table className="table">
            <tbody className="divide-y divide-line">
              {data.top_selling_products.map((item) => (
                <tr key={item.label}>
                  <td>{item.label}</td>
                  <td className="text-right font-semibold">{item.value} sold</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
