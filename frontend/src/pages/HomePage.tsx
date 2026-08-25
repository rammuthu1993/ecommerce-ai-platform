import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, Package, Bot, Zap } from 'lucide-react';
import { productService } from '../services/productService';
import { Product } from '../types';

export const HomePage: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    productService
      .getProducts({ limit: 4 })
      .then((res) => setFeaturedProducts(res.data))
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      {/* Hero Section */}
      <section
        className="glass-panel animate-fade-in"
        style={{
          padding: '4rem 3rem',
          borderRadius: 'var(--radius-lg)',
          background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95))',
          position: 'relative',
          overflow: 'hidden',
          marginBottom: '3rem',
          boxShadow: 'var(--shadow-glow)',
        }}
      >
        <div style={{ maxWidth: '640px' }}>
          <span
            style={{
              padding: '0.35rem 0.85rem',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(99, 102, 241, 0.2)',
              color: 'var(--accent-primary)',
              fontSize: '0.8rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem',
              marginBottom: '1rem',
            }}
          >
            <Sparkles size={14} /> AI-Powered Commerce Platform
          </span>
          <h1
            style={{
              fontSize: '3rem',
              lineHeight: 1.15,
              marginBottom: '1.25rem',
              fontFamily: 'var(--font-heading)',
            }}
          >
            Next-Gen Shopping <br />
            <span className="gradient-text">Driven by AI Intelligence</span>
          </h1>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
            Discover top-tier tech products, real-time inventory tracking, vector policy retrieval, and autonomous AI Agent assistance.
          </p>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <Link
              to="/products"
              style={{
                padding: '0.85rem 1.75rem',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                color: '#fff',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              Explore Catalog <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Products Grid */}
      <section style={{ marginBottom: '4rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Featured Products</h2>
          <Link to="/products" style={{ color: 'var(--accent-primary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            View All Catalog <ArrowRight size={16} />
          </Link>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '1.5rem' }}>
          {featuredProducts.map((prod) => (
            <div
              key={prod.id}
              className="glass-panel glass-panel-hover"
              style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column' }}
            >
              <div
                style={{
                  height: '180px',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(255, 255, 255, 0.03)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '1rem',
                  color: 'var(--accent-primary)',
                }}
              >
                <Package size={48} />
              </div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.35rem' }}>{prod.name}</h3>
              <p style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--accent-emerald)', marginTop: 'auto' }}>
                ${prod.price.toFixed(2)}
              </p>
              <Link
                to={`/products/${prod.id}`}
                style={{
                  marginTop: '1rem',
                  padding: '0.65rem',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(99, 102, 241, 0.15)',
                  color: 'var(--accent-primary)',
                  textAlign: 'center',
                  fontWeight: 600,
                }}
              >
                View Details
              </Link>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
