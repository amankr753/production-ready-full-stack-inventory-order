import { Plus, Search, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import EmptyState from "../components/EmptyState";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import api from "../services/api";

const blank = { full_name: "", email: "", phone_number: "", address: "", city: "", state: "", country: "", postal_code: "", customer_type: "retail" };

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [query, setQuery] = useState("");
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(blank);

  async function load() {
    const { data } = await api.get("/customers", { params: { search: query || undefined, size: 50 } });
    setCustomers(data.items);
  }
  useEffect(() => { load(); }, []);

  async function save(event) {
    event.preventDefault();
    try {
      await api.post("/customers", form);
      toast.success("Customer saved");
      setModal(false);
      setForm(blank);
      load();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to save customer");
    }
  }

  async function remove(id) {
    if (!confirm("Delete this customer?")) return;
    await api.delete(`/customers/${id}`);
    toast.success("Customer deleted");
    load();
  }

  return (
    <>
      <PageHeader title="Customers" description="Maintain customer records and contact data." action={<button className="btn btn-primary" onClick={() => setModal(true)}><Plus className="h-4 w-4" />Add customer</button>} />
      <div className="panel mb-4 flex gap-2 p-3">
        <div className="relative flex-1"><Search className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-slate-400" /><input className="pl-9" placeholder="Search customers" value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()} /></div>
        <button className="btn btn-secondary" onClick={load}>Search</button>
      </div>
      {customers.length ? (
        <div className="panel overflow-x-auto">
          <table className="table">
            <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Location</th><th>Type</th><th></th></tr></thead>
            <tbody className="divide-y divide-line">
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td className="font-semibold text-ink">{customer.full_name}</td>
                  <td>{customer.email}</td>
                  <td>{customer.phone_number || "-"}</td>
                  <td>{[customer.city, customer.country].filter(Boolean).join(", ") || "-"}</td>
                  <td className="capitalize">{customer.customer_type}</td>
                  <td className="text-right"><button className="btn btn-secondary p-2 text-danger" onClick={() => remove(customer.id)} aria-label="Delete customer"><Trash2 className="h-4 w-4" /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <EmptyState title="No customers yet" text="Create a customer before placing orders." />}
      <Modal title="Add customer" open={modal} onClose={() => setModal(false)}>
        <form onSubmit={save} className="grid gap-3 sm:grid-cols-2">
          {Object.keys(blank).map((field) => <input key={field} placeholder={field.replaceAll("_", " ")} value={form[field] || ""} onChange={(e) => setForm({ ...form, [field]: e.target.value })} required={["full_name", "email"].includes(field)} type={field === "email" ? "email" : "text"} />)}
          <div className="flex justify-end gap-2 sm:col-span-2"><button type="button" className="btn btn-secondary" onClick={() => setModal(false)}>Cancel</button><button className="btn btn-primary">Save</button></div>
        </form>
      </Modal>
    </>
  );
}
