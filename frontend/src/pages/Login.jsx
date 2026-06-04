import { Eye, LockKeyhole } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "admin@example.com", password: "Password123" });
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      await login(form.email, form.password);
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen bg-slate-50 lg:grid-cols-[1fr_1.1fr]">
      <section className="flex items-center justify-center p-6">
        <form onSubmit={submit} className="panel w-full max-w-md p-6">
          <div className="mb-6">
            <div className="mb-4 inline-flex rounded-md bg-blue-50 p-3 text-brand">
              <LockKeyhole className="h-6 w-6" />
            </div>
            <h1 className="text-2xl font-semibold text-ink">Sign in to StockOps</h1>
            <p className="mt-1 text-sm text-slate-500">Manage products, orders, stock, and revenue from one workspace.</p>
          </div>
          <label className="mb-3 block text-sm font-medium text-slate-700">
            Email
            <input className="mt-1" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} type="email" required />
          </label>
          <label className="mb-4 block text-sm font-medium text-slate-700">
            Password
            <input className="mt-1" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} type="password" required />
          </label>
          <button className="btn btn-primary w-full" disabled={loading}>
            <Eye className="h-4 w-4" />
            {loading ? "Signing in..." : "Sign in"}
          </button>
          <p className="mt-4 text-center text-sm text-slate-500">
            New team? <Link className="font-semibold text-brand" to="/register">Create account</Link>
          </p>
        </form>
      </section>
      <section className="hidden bg-[linear-gradient(135deg,#eef4ff,#f8fafc_45%,#ecfeff)] p-10 lg:flex lg:flex-col lg:justify-between">
        <div className="max-w-xl">
          <p className="text-sm font-semibold uppercase text-brand">Operations dashboard</p>
          <h2 className="mt-4 text-5xl font-bold leading-tight text-ink">Inventory clarity for fast moving teams.</h2>
          <p className="mt-5 text-lg text-slate-600">Track stock movement, protect margins, and keep orders moving without spreadsheet drift.</p>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {["Stock alerts", "Revenue trends", "Order flow"].map((item) => (
            <div className="rounded-lg border border-white/80 bg-white/70 p-4 shadow-sm" key={item}>
              <p className="text-sm font-semibold text-ink">{item}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
