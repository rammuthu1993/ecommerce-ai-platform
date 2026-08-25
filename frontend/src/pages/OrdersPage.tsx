import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBag, FileText, CheckCircle2, Clock } from 'lucide-react';
import { orderService } from '../services/orderService';
import { Order } from '../types';
import { Badge } from '../components/common/Badge';

export const OrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    orderService
      .getOrders()
      .then((res) => setOrders(res.data))
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      <h1 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.25rem' }}>My Orders</h1>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Track your purchase orders and invoice details
      </p>

      {isLoading ? (
        <div style={{ padding: '3rem', textAlign: 'center' }}>Loading orders...</div>
      ) : orders.length === 0 ? (
        <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>No orders found.</div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {orders.map((ord) => (
            <div key={ord.id} className="glass-panel" style={{ padding: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.75rem' }}>
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Order #{ord.order_number}</h3>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{ord.created_at}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <Badge variant={ord.status === 'PAID' || ord.status === 'DELIVERED' ? 'success' : 'warning'}>
                    {ord.status}
                  </Badge>
                  <span style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>
                    ${ord.total_amount.toFixed(2)}
                  </span>
                </div>
              </div>

              {/* Status Timeline */}
              <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <CheckCircle2 size={16} color="var(--accent-emerald)" /> Created
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <Clock size={16} color="var(--accent-amber)" /> Status: {ord.status}
                </div>
                <Link
                  to={`/invoices/${ord.id}`}
                  style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--accent-primary)', fontWeight: 600 }}
                >
                  <FileText size={16} /> View Invoice
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
