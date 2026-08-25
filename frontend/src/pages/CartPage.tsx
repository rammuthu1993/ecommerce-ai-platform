import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, Trash2, ArrowRight } from 'lucide-react';
import { useCart } from '../context/CartContext';

export const CartPage: React.FC = () => {
  const { cartItems, updateQuantity, removeFromCart, clearCart, subtotal } = useCart();
  const navigate = useNavigate();

  if (cartItems.length === 0) {
    return (
      <div style={{ maxWidth: '600px', margin: '4rem auto', textAlign: 'center', padding: '2rem' }}>
        <div style={{ width: '64px', height: '64px', borderRadius: 'var(--radius-full)', background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
          <ShoppingBag size={32} />
        </div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: '0.5rem' }}>Your Cart is Empty</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Looks like you haven't added any products yet.</p>
        <Link
          to="/products"
          style={{ padding: '0.75rem 1.5rem', borderRadius: 'var(--radius-md)', background: 'var(--accent-primary)', color: '#fff', fontWeight: 600 }}
        >
          Browse Products
        </Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.25rem', fontWeight: 800 }}>Shopping Cart</h1>
        <button onClick={clearCart} style={{ background: 'transparent', color: 'var(--accent-rose)', fontSize: '0.85rem' }}>
          Clear All Items
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem' }}>
        {/* Cart Items List */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          {cartItems.map((item) => (
            <div
              key={item.product_id}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '1rem 0',
                borderBottom: '1px solid rgba(255,255,255,0.05)',
              }}
            >
              <div>
                <h4 style={{ fontSize: '1rem', fontWeight: 600 }}>{item.product_name}</h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>
                  ${item.unit_price.toFixed(2)} each
                </p>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)' }}>
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                    style={{ padding: '0.35rem 0.65rem', background: 'transparent', color: 'var(--text-primary)' }}
                  >
                    -
                  </button>
                  <span style={{ padding: '0 0.5rem', fontSize: '0.85rem', fontWeight: 600 }}>{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                    style={{ padding: '0.35rem 0.65rem', background: 'transparent', color: 'var(--text-primary)' }}
                  >
                    +
                  </button>
                </div>

                <span style={{ fontSize: '1rem', fontWeight: 700, width: '80px', textAlign: 'right' }}>
                  ${item.line_total.toFixed(2)}
                </span>

                <button onClick={() => removeFromCart(item.product_id)} style={{ background: 'transparent', color: 'var(--accent-rose)' }}>
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Summary Box */}
        <div className="glass-panel" style={{ padding: '1.5rem', height: 'fit-content' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem' }}>Order Summary</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            <span>Subtotal</span>
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>${subtotal.toFixed(2)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            <span>Estimated Shipping</span>
            <span style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>FREE</span>
          </div>
          <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1rem', marginTop: '1rem', display: 'flex', justifyContent: 'space-between', fontSize: '1.2rem', fontWeight: 800 }}>
            <span>Total</span>
            <span style={{ color: 'var(--accent-emerald)' }}>${subtotal.toFixed(2)}</span>
          </div>

          <button
            onClick={() => navigate('/checkout')}
            style={{
              width: '100%',
              padding: '0.85rem',
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: '#fff',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              marginTop: '1.5rem',
            }}
          >
            Proceed to Checkout <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};
