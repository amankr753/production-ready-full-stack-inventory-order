import { UserPlus } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", role: "staff" });

  async function submit(event) {
    event.preventDefault();
    try {
      await register(form);
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Registration failed");
    }
  }

  return (
    <div className="screen-center p-4">
      <form onSubmit={submit} className="panel w-full max-w-md p-6">
        <div className="mb-5">
          <div className="mb-4 inline-flex rounded-md bg-blue-50 p-3 text-brand">
            <UserPlus className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-semibold text-ink">Create an account</h1>
        </div>
        <div className="space-y-3">
          <input placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required />
          <input placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input placeholder="Password" type="password" minLength={8} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="staff">Staff</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <button className="btn btn-primary mt-5 w-full">Create account</button>
        <p className="mt-4 text-center text-sm text-slate-500">
          Already registered? <Link className="font-semibold text-brand" to="/login">Sign in</Link>
        </p>
      </form>
    </div>
  );
}
