import React from 'react';
import { Sparkles, ShieldCheck, Truck, RotateCcw } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer
      style={{
        marginTop: 'auto',
        borderTop: '1px solid var(--border-color)',
        background: 'var(--bg-secondary)',
        padding: '3rem 2rem 2rem',
      }}
    >
      <div
        style={{
          maxWidth: '1280px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '2rem',
          paddingBottom: '2.5rem',
          borderBottom: '1px solid var(--border-color)',
        }}
      >
        {/* Features */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{ padding: '0.75rem', borderRadius: 'var(--radius-md)', background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>
            <Truck size={24} />
          </div>
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600 }}>Free Express Shipping</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>On all orders over $50.00</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{ padding: '0.75rem', borderRadius: 'var(--radius-md)', background: 'rgba(16,185,129,0.15)', color: 'var(--accent-emerald)' }}>
            <ShieldCheck size={24} />
          </div>
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600 }}>256-bit Encrypted</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>100% Secure Checkout</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{ padding: '0.75rem', borderRadius: 'var(--radius-md)', background: 'rgba(244,63,94,0.15)', color: 'var(--accent-rose)' }}>
            <RotateCcw size={24} />
          </div>
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600 }}>30-Day Returns</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Hassle-free refund policy</p>
          </div>
        </div>
      </div>

      <div
        style={{
          maxWidth: '1280px',
          margin: '0 auto',
          paddingTop: '1.5rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          fontSize: '0.85rem',
          color: 'var(--text-muted)',
        }}
      >
        <p>© 2026 E-Commerce AI Platform. All rights reserved.</p>
        <p>Powered by Python + React + Vector RAG & AI Agent</p>
      </div>
    </footer>
  );
};
