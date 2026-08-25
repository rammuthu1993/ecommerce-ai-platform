import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FileText, ArrowLeft, Printer, CheckCircle } from 'lucide-react';
import { orderService } from '../services/orderService';
import { Order } from '../types';

export const InvoicePage: React.FC = () => {
  const { orderId } = useParams<{ orderId: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (orderId) {
      orderService
        .getOrder(parseInt(orderId))
        .then((res) => setOrder(res.data))
        .catch(() => {})
        .finally(() => setIsLoading(false));
    }
  }, [orderId]);

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading invoice document...</div>;
  if (!order) return <div style={{ padding: '4rem', textAlign: 'center' }}>Invoice not found.</div>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <Link to="/orders" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)' }}>
          <ArrowLeft size={16} /> Back to Orders
        </Link>
        <button
          onClick={() => window.print()}
          style={{
            padding: '0.5rem 1rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(255,255,255,0.08)',
            color: 'var(--text-primary)',
            fontSize: '0.85rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.35rem',
          }}
        >
          <Printer size={16} /> Print Invoice
        </button>
      </div>

      <div className="glass-panel" style={{ padding: '2.5rem', background: '#1e293b' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem', marginBottom: '1.5rem' }}>
          <div>
            <h1 className="gradient-text" style={{ fontSize: '1.75rem', fontWeight: 800 }}>Ecommerce.AI Platform</h1>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Official Tax Invoice Document</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>INVOICE</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>#{order.order_number}</p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Date: {order.created_at}</p>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', fontSize: '0.85rem' }}>
          <div>
            <span style={{ color: 'var(--text-muted)', display: 'block', marginBottom: '0.25rem' }}>Billed To:</span>
            <strong>Customer #{order.customer_id}</strong>
          </div>
          <div style={{ textAlign: 'right' }}>
            <span style={{ color: 'var(--text-muted)', display: 'block', marginBottom: '0.25rem' }}>Payment Status:</span>
            <strong style={{ color: 'var(--accent-emerald)' }}>{order.status}</strong>
          </div>
        </div>

        {/* Invoice Summary */}
        <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
            <span>Subtotal</span>
            <span>${order.subtotal.toFixed(2)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
            <span>Tax (10%)</span>
            <span>${(order.tax_amount || 0).toFixed(2)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.25rem', fontWeight: 800, borderTop: '1px solid var(--border-color)', paddingTop: '1rem', marginTop: '0.5rem' }}>
            <span>Total Paid</span>
            <span style={{ color: 'var(--accent-emerald)' }}>${order.total_amount.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
