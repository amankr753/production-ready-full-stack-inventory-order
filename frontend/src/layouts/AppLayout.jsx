import { BarChart3, Boxes, ClipboardList, LogOut, Menu, Package, Users } from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const nav = [
  { to: "/dashboard", label: "Dashboard", icon: BarChart3 },
  { to: "/products", label: "Products", icon: Package },
  { to: "/customers", label: "Customers", icon: Users },
  { to: "/orders", label: "Orders", icon: ClipboardList },
  { to: "/inventory", label: "Inventory", icon: Boxes }
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50">
      <aside className={`fixed inset-y-0 left-0 z-40 w-64 border-r border-line bg-white transition ${open ? "translate-x-0" : "-translate-x-full md:translate-x-0"}`}>
        <div className="border-b border-line px-5 py-4">
          <p className="text-lg font-bold text-ink">StockOps</p>
          <p className="text-xs text-slate-500">Inventory Control</p>
        </div>
        <nav className="space-y-1 p-3">
          {nav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium ${isActive ? "bg-blue-50 text-brand" : "text-slate-600 hover:bg-slate-50"}`
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="md:pl-64">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-line bg-white px-4 md:px-6">
          <button className="btn btn-secondary p-2 md:hidden" onClick={() => setOpen(true)} aria-label="Open navigation">
            <Menu className="h-5 w-5" />
          </button>
          <div className="ml-auto flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-ink">{user?.full_name}</p>
              <p className="text-xs capitalize text-slate-500">{user?.role}</p>
            </div>
            <button className="btn btn-secondary" onClick={logout}>
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </header>
        <main className="p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
