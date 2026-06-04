import { AlertTriangle, Boxes, History } from "lucide-react";
import { useEffect, useState } from "react";

import EmptyState from "../components/EmptyState";
import MetricCard from "../components/MetricCard";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";
import api from "../services/api";
import { shortDate } from "../utils/format";

export default function Inventory() {
  const [logs, setLogs] = useState([]);
  const [low, setLow] = useState([]);
  const [out, setOut] = useState([]);

  useEffect(() => {
    Promise.all([api.get("/inventory/logs"), api.get("/inventory/low-stock"), api.get("/inventory/out-of-stock")]).then(([logRes, lowRes, outRes]) => {
      setLogs(logRes.data.items);
      setLow(lowRes.data);
      setOut(outRes.data);
    });
  }, []);

  return (
    <>
      <PageHeader title="Inventory" description="Audit stock movements and respond to reorder alerts." />
      <div className="mb-5 grid gap-4 sm:grid-cols-3">
        <MetricCard title="Movement logs" value={logs.length} icon={History} />
        <MetricCard title="Low stock" value={low.length} icon={AlertTriangle} tone="warning" />
        <MetricCard title="Out of stock" value={out.length} icon={Boxes} tone="danger" />
      </div>
      <div className="grid gap-5 xl:grid-cols-[1fr_1.3fr]">
        <div className="space-y-5">
          <div className="panel overflow-hidden">
            <h2 className="border-b border-line p-4 font-semibold text-ink">Low stock alerts</h2>
            <div className="divide-y divide-line">
              {low.map((product) => (
                <div className="flex items-center justify-between p-4" key={product.id}>
                  <div><p className="font-semibold text-ink">{product.product_name}</p><p className="text-xs text-slate-500">Reorder at {product.reorder_level}</p></div>
                  <StatusBadge status={product.stock_status} />
                </div>
              ))}
              {!low.length ? <div className="p-4"><EmptyState title="No low stock" text="All stocked products are above reorder levels." /></div> : null}
            </div>
          </div>
          <div className="panel overflow-hidden">
            <h2 className="border-b border-line p-4 font-semibold text-ink">Out of stock</h2>
            <div className="divide-y divide-line">
              {out.map((product) => <div className="p-4 font-semibold text-ink" key={product.id}>{product.product_name}</div>)}
              {!out.length ? <div className="p-4"><EmptyState title="No outages" text="No product is currently out of stock." /></div> : null}
            </div>
          </div>
        </div>
        <div className="panel overflow-x-auto">
          <table className="table">
            <thead><tr><th>Date</th><th>Product</th><th>Action</th><th>Change</th><th>Balance</th><th>Reference</th></tr></thead>
            <tbody className="divide-y divide-line">
              {logs.map((log) => (
                <tr key={log.id}>
                  <td>{shortDate(log.created_at)}</td>
                  <td className="font-semibold text-ink">{log.product?.product_name || log.product_id}</td>
                  <td><StatusBadge status={log.action} /></td>
                  <td className={log.quantity_change < 0 ? "text-danger" : "text-success"}>{log.quantity_change}</td>
                  <td>{log.new_quantity}</td>
                  <td>{log.reference || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
