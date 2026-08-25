import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, CheckCircle } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { orderService } from '../services/orderService';

export const CheckoutPage: React.FC = () => {
  const { cartItems, subtotal, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const customerId = user?.id || 1;
      const res = await orderService.checkout({ customer_id: customerId });
      clearCart();
      navigate('/orders');
    } catch (err: any) {
      setError(err.message || 'Checkout failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      <h1 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.25rem' }}>Express Checkout</h1>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Complete your order securely
      </p>

      {error && (
        <div style={{ padding: '0.75rem 1rem', borderRadius: 'var(--radius-md)', background: 'rgba(244,63,94,0.15)', color: 'var(--accent-rose)', marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      <div className="glass-panel" style={{ padding: '2rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem' }}>Order Items</h3>
        <div style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
          {cartItems.map((item) => (
            <div key={item.product_id} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
              <span>
                {item.product_name} x {item.quantity}
              </span>
              <span style={{ fontWeight: 600 }}>${item.line_total.toFixed(2)}</span>
            </div>
          ))}
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.25rem', fontWeight: 800, marginBottom: '2rem' }}>
          <span>Total Amount</span>
          <span style={{ color: 'var(--accent-emerald)' }}>${subtotal.toFixed(2)}</span>
        </div>

        <button
          onClick={handlePlaceOrder}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '1rem',
            borderRadius: 'var(--radius-md)',
            background: 'linear-gradient(135deg, #10b981, #6366f1)',
            color: '#fff',
            fontWeight: 700,
            fontSize: '1rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
          }}
        >
          <CheckCircle size={20} /> {isLoading ? 'Processing Order...' : 'Confirm Order & Checkout'}
        </button>
      </div>
    </div>
  );
};
