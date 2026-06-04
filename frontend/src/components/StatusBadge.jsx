export default function StatusBadge({ status }) {
  const tone = {
    in_stock: "bg-teal-50 text-success",
    low_stock: "bg-amber-50 text-warning",
    out_of_stock: "bg-red-50 text-danger",
    pending: "bg-amber-50 text-warning",
    processing: "bg-blue-50 text-brand",
    completed: "bg-teal-50 text-success",
    cancelled: "bg-red-50 text-danger",
    paid: "bg-teal-50 text-success",
    unpaid: "bg-slate-100 text-slate-600",
    refunded: "bg-purple-50 text-purple-700"
  };
  return <span className={`badge ${tone[status] || "bg-slate-100 text-slate-600"}`}>{String(status).replaceAll("_", " ")}</span>;
}
