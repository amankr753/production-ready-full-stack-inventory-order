import { Plus, Receipt, Trash2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";

import EmptyState from "../components/EmptyState";
import Modal from "../components/Modal";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";
import api from "../services/api";
import { money, shortDate } from "../utils/format";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ customer_id: "", payment_status: "unpaid", payment_method: "card", tax_amount: 0, discount: 0, items: [{ product_id: "", quantity: 1 }] });

  async function load() {
    const [orderRes, customerRes, productRes] = await Promise.all([
      api.get("/orders", { params: { size: 50 } }),
      api.get("/customers", { params: { size: 100 } }),
      api.get("/products", { params: { size: 100 } })
    ]);
    setOrders(orderRes.data.items);
    setCustomers(customerRes.data.items);
    setProducts(productRes.data.items);
  }
  useEffect(() => { load(); }, []);

  const estimate = useMemo(() => {
    const subtotal = form.items.reduce((sum, item) => {
      const product = products.find((entry) => entry.id === Number(item.product_id));
      return sum + Number(item.quantity || 0) * Number(product?.selling_price || 0);
    }, 0);
    return Math.max(subtotal + Number(form.tax_amount || 0) - Number(form.discount || 0), 0);
  }, [form, products]);

  async function save(event) {
    event.preventDefault();
    try {
      await api.post("/orders", {
        ...form,
        customer_id: Number(form.customer_id),
        tax_amount: Number(form.tax_amount),
        discount: Number(form.discount),
        items: form.items.map((item) => ({ product_id: Number(item.product_id), quantity: Number(item.quantity) }))
      });
      toast.success("Order created");
      setModal(false);
      load();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Unable to create order");
    }
  }

  async function updateStatus(order, status) {
    await api.put(`/orders/${order.id}`, { order_status: status, payment_status: order.payment_status });
    toast.success("Order updated");
    load();
  }

  async function cancel(order) {
    if (!confirm("Cancel and delete this order? Stock will be restored.")) return;
    await api.delete(`/orders/${order.id}`);
    toast.success("Order cancelled");
    load();
  }

  return (
    <>
      <PageHeader title="Orders" description="Create orders, calculate totals, and track fulfillment status." action={<button className="btn btn-primary" onClick={() => setModal(true)}><Plus className="h-4 w-4" />Create order</button>} />
      {orders.length ? (
        <div className="panel overflow-x-auto">
          <table className="table">
            <thead><tr><th>Order</th><th>Customer</th><th>Date</th><th>Status</th><th>Payment</th><th>Total</th><th></th></tr></thead>
            <tbody className="divide-y divide-line">
              {orders.map((order) => (
                <tr key={order.id}>
                  <td className="font-semibold text-ink">{order.order_number}</td>
                  <td>{order.customer?.full_name || order.customer_id}</td>
                  <td>{shortDate(order.created_at)}</td>
                  <td>
                    <select className="w-36" value={order.order_status} onChange={(e) => updateStatus(order, e.target.value)}>
                      {["pending", "processing", "completed", "cancelled"].map((status) => <option key={status}>{status}</option>)}
                    </select>
                  </td>
                  <td><StatusBadge status={order.payment_status} /></td>
                  <td className="font-semibold">{money(order.total_amount)}</td>
                  <td className="text-right"><button className="btn btn-secondary p-2 text-danger" onClick={() => cancel(order)} aria-label="Cancel order"><Trash2 className="h-4 w-4" /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <EmptyState title="No orders yet" text="Create an order to deduct stock and generate revenue." />}
      <Modal title="Create order" open={modal} onClose={() => setModal(false)}>
        <form onSubmit={save} className="space-y-4">
          <select value={form.customer_id} onChange={(e) => setForm({ ...form, customer_id: e.target.value })} required>
            <option value="">Select customer</option>
            {customers.map((customer) => <option key={customer.id} value={customer.id}>{customer.full_name}</option>)}
          </select>
          <div className="grid gap-3 sm:grid-cols-3">
            <select value={form.payment_status} onChange={(e) => setForm({ ...form, payment_status: e.target.value })}><option>unpaid</option><option>paid</option><option>refunded</option></select>
            <input placeholder="Payment method" value={form.payment_method} onChange={(e) => setForm({ ...form, payment_method: e.target.value })} />
            <div className="rounded-md border border-line bg-slate-50 px-3 py-2 text-sm font-semibold">{money(estimate)}</div>
          </div>
          <div className="space-y-2">
            {form.items.map((item, index) => (
              <div className="grid gap-2 sm:grid-cols-[1fr_120px]" key={index}>
                <select value={item.product_id} onChange={(e) => setForm({ ...form, items: form.items.map((entry, i) => i === index ? { ...entry, product_id: e.target.value } : entry) })} required>
                  <option value="">Select product</option>
                  {products.map((product) => <option key={product.id} value={product.id}>{product.product_name} ({product.quantity_in_stock} available)</option>)}
                </select>
                <input type="number" min="1" value={item.quantity} onChange={(e) => setForm({ ...form, items: form.items.map((entry, i) => i === index ? { ...entry, quantity: e.target.value } : entry) })} />
              </div>
            ))}
            <button type="button" className="btn btn-secondary" onClick={() => setForm({ ...form, items: [...form.items, { product_id: "", quantity: 1 }] })}>Add line</button>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <input type="number" min="0" step="0.01" placeholder="Tax" value={form.tax_amount} onChange={(e) => setForm({ ...form, tax_amount: e.target.value })} />
            <input type="number" min="0" step="0.01" placeholder="Discount" value={form.discount} onChange={(e) => setForm({ ...form, discount: e.target.value })} />
          </div>
          <div className="flex justify-end gap-2"><button type="button" className="btn btn-secondary" onClick={() => setModal(false)}>Cancel</button><button className="btn btn-primary"><Receipt className="h-4 w-4" />Create</button></div>
        </form>
      </Modal>
    </>
  );
}
