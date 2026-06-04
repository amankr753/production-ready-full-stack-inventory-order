export default function MetricCard({ title, value, icon: Icon, tone = "brand" }) {
  const tones = {
    brand: "bg-blue-50 text-brand",
    success: "bg-teal-50 text-success",
    warning: "bg-amber-50 text-warning",
    danger: "bg-red-50 text-danger"
  };

  return (
    <div className="panel p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <p className="mt-2 text-2xl font-semibold text-ink">{value}</p>
        </div>
        {Icon ? (
          <div className={`rounded-md p-2 ${tones[tone]}`}>
            <Icon className="h-5 w-5" />
          </div>
        ) : null}
      </div>
    </div>
  );
}
