import { Edit, Plus, Search, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import EmptyState from "../components/EmptyState";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";
import api from "../services/api";
import { money } from "../utils/format";

const blank = {
  product_name: "",
  sku_code: "",
  description: "",
  category: "",
  brand: "",
  purchase_price: 0,
  selling_price: 0,
  quantity_in_stock: 0,
  reorder_level: 5,
  product_image: ""
};

export default function Products() {
  const [products, setProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(blank);
  const [editing, setEditing] = useState(null);

  async function load() {
    const { data } = await api.get("/products", { params: { search: query || undefined, size: 50 } });
    setProducts(data.items);
  }

  useEffect(() => {
    load();
  }, []);

  function openForm(product) {
    setEditing(product || null);
    setForm(product || blank);
    setModal(true);
  }

  async function save(event) {
    event.preventDefault();
    const payload = { ...form, purchase_price: Number(form.purchase_price), selling_price: Number(form.selling_price), quantity_in_stock: Number(form.quantity_in_stock), reorder_level: Number(form.reorder_level) };
    try {
      if (editing) await api.put(`/products/${editing.id}`, payload);
      else await api.post("/products", payload);
      toast.success("Product saved");
      setModal(false);
      load();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to save product");
    }
  }

  async function remove(id) {
    if (!confirm("Delete this product?")) return;
    await api.delete(`/products/${id}`);
    toast.success("Product deleted");
    load();
  }

  return (
    <>
      <PageHeader title="Products" description="Manage SKUs, pricing, stock thresholds, and catalog data." action={<button className="btn btn-primary" onClick={() => openForm()}><Plus className="h-4 w-4" />Add product</button>} />
      <div className="panel mb-4 flex gap-2 p-3">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
          <input className="pl-9" placeholder="Search name, SKU, or brand" value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()} />
        </div>
        <button className="btn btn-secondary" onClick={load}>Search</button>
      </div>
      {products.length ? (
        <div className="panel overflow-x-auto">
          <table className="table">
            <thead><tr><th>Product</th><th>SKU</th><th>Category</th><th>Price</th><th>Stock</th><th>Status</th><th></th></tr></thead>
            <tbody className="divide-y divide-line">
              {products.map((product) => (
                <tr key={product.id}>
                  <td><p className="font-semibold text-ink">{product.product_name}</p><p className="text-xs text-slate-500">{product.brand}</p></td>
                  <td>{product.sku_code}</td>
                  <td>{product.category}</td>
                  <td>{money(product.selling_price)}</td>
                  <td>{product.quantity_in_stock}</td>
                  <td><StatusBadge status={product.stock_status} /></td>
                  <td className="flex justify-end gap-2">
                    <button className="btn btn-secondary p-2" onClick={() => openForm(product)} aria-label="Edit product"><Edit className="h-4 w-4" /></button>
                    <button className="btn btn-secondary p-2 text-danger" onClick={() => remove(product.id)} aria-label="Delete product"><Trash2 className="h-4 w-4" /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <EmptyState title="No products yet" text="Add a SKU to start tracking stock movement." />}
      <Modal title={editing ? "Edit product" : "Add product"} open={modal} onClose={() => setModal(false)}>
        <form onSubmit={save} className="grid gap-3 sm:grid-cols-2">
          {["product_name", "sku_code", "category", "brand", "product_image"].map((field) => <input key={field} placeholder={field.replaceAll("_", " ")} value={form[field] || ""} onChange={(e) => setForm({ ...form, [field]: e.target.value })} required={["product_name", "sku_code", "category"].includes(field)} />)}
          {["purchase_price", "selling_price", "quantity_in_stock", "reorder_level"].map((field) => <input key={field} type="number" min="0" step="0.01" placeholder={field.replaceAll("_", " ")} value={form[field]} onChange={(e) => setForm({ ...form, [field]: e.target.value })} />)}
          <textarea className="sm:col-span-2" rows="3" placeholder="Description" value={form.description || ""} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <div className="flex justify-end gap-2 sm:col-span-2"><button type="button" className="btn btn-secondary" onClick={() => setModal(false)}>Cancel</button><button className="btn btn-primary">Save</button></div>
        </form>
      </Modal>
    </>
  );
}
