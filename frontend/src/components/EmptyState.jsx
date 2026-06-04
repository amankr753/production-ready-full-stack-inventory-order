import { PackageOpen } from "lucide-react";

export default function EmptyState({ title = "No records found", text = "Create a record or adjust your filters." }) {
  return (
    <div className="flex min-h-48 flex-col items-center justify-center rounded-lg border border-dashed border-line bg-white p-8 text-center">
      <PackageOpen className="mb-3 h-8 w-8 text-slate-400" />
      <h3 className="font-semibold text-ink">{title}</h3>
      <p className="mt-1 text-sm text-slate-500">{text}</p>
    </div>
  );
}
