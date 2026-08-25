import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, Sparkles, Search, User, LogOut, LayoutDashboard, ShieldCheck, Box, Tag, Warehouse } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import { RAGSearchModal } from '../ai/RAGSearchModal';

export const Navbar: React.FC = () => {
  const { user, token, isAuthenticated, isLoading, logout, isManager, isAdmin } = useAuth();
  const { itemCount } = useCart();
  const navigate = useNavigate();
  const hasSession = isAuthenticated || !!token;

  const [isRAGOpen, setIsRAGOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <>
      <nav
        className="glass-panel"
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          borderRadius: 0,
          borderLeft: 'none',
          borderRight: 'none',
          borderTop: 'none',
          padding: '0.85rem 2rem',
        }}
      >
        <div
          style={{
            maxWidth: '1280px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          {/* Brand Logo */}
          <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <div
              style={{
                width: '38px',
                height: '38px',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                boxShadow: 'var(--shadow-glow)',
              }}
            >
              <Sparkles size={22} />
            </div>
            <span
              className="gradient-text"
              style={{ fontSize: '1.35rem', fontWeight: 800, fontFamily: 'var(--font-heading)' }}
            >
              Ecommerce.AI
            </span>
          </Link>

          {/* Navigation Links */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.75rem' }}>
            <Link to="/products" style={{ color: 'var(--text-primary)', fontWeight: 500 }}>
              Catalog
            </Link>

            {isAuthenticated && (
              <Link
                to="/admin/products"
                style={{
                  color: 'var(--accent-primary)',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.35rem',
                  fontSize: '0.9rem',
                }}
              >
                <Box size={16} /> Manage Products
              </Link>
            )}

            {isAuthenticated && isManager && (
              <>
                <Link
                  to="/admin/dashboard"
                  style={{
                    color: 'var(--text-secondary)',
                    fontWeight: 500,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    fontSize: '0.9rem',
                  }}
                >
                  <LayoutDashboard size={16} /> Admin Portal
                </Link>
                <Link
                  to="/admin/inventory"
                  style={{
                    color: 'var(--text-secondary)',
                    fontWeight: 500,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    fontSize: '0.9rem',
                  }}
                >
                  <Warehouse size={16} /> Stock
                </Link>
              </>
            )}
          </div>

          {/* Action Tools: RAG Policy Search, Cart, Auth State */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            {/* RAG Policy Search Trigger */}
            <button
              onClick={() => setIsRAGOpen(true)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.5rem 0.9rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.05)',
                color: 'var(--text-secondary)',
                border: '1px solid var(--border-color)',
                fontSize: '0.85rem',
              }}
            >
              <Search size={16} />
              <span>🔍 RAG Policy Search</span>
            </button>

            {/* Shopping Cart Badge */}
            <Link
              to="/cart"
              style={{
                position: 'relative',
                padding: '0.55rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.05)',
                color: 'var(--text-primary)',
                display: 'flex',
                alignItems: 'center',
              }}
            >
              <ShoppingBag size={20} />
              {itemCount > 0 && (
                <span
                  style={{
                    position: 'absolute',
                    top: '-6px',
                    right: '-6px',
                    background: 'var(--accent-rose)',
                    color: '#fff',
                    borderRadius: 'var(--radius-full)',
                    width: '20px',
                    height: '20px',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  {itemCount}
                </span>
              )}
            </Link>

            {/* Auth Menu: Hide Sign In / Register when authenticated */}
            {hasSession || isLoading ? (
              <div style={{ position: 'relative' }}>
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    padding: '0.45rem 0.85rem',
                    borderRadius: 'var(--radius-md)',
                    background: 'linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.2))',
                    color: 'var(--text-primary)',
                    border: '1px solid var(--border-glow)',
                  }}
                >
                  <User size={18} color="var(--accent-primary)" />
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>{user?.username}</span>
                  {isManager && (
                    <span
                      style={{
                        fontSize: '0.7rem',
                        padding: '0.15rem 0.4rem',
                        borderRadius: 'var(--radius-sm)',
                        background: 'var(--accent-primary)',
                        color: '#fff',
                        fontWeight: 700,
                      }}
                    >
                      ADMIN
                    </span>
                  )}
                </button>

                {dropdownOpen && (
                  <div
                    className="glass-panel animate-fade-in"
                    style={{
                      position: 'absolute',
                      right: 0,
                      marginTop: '0.5rem',
                      width: '200px',
                      padding: '0.5rem',
                      boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
                      zIndex: 200,
                    }}
                  >
                    <div style={{ padding: '0.5rem', borderBottom: '1px solid var(--border-color)', marginBottom: '0.35rem' }}>
                      <p style={{ fontSize: '0.85rem', fontWeight: 700 }}>{user?.username}</p>
                      <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{user?.email}</p>
                    </div>

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        navigate('/orders');
                      }}
                      style={{
                        width: '100%',
                        textAlign: 'left',
                        padding: '0.5rem',
                        background: 'transparent',
                        color: 'var(--text-primary)',
                        fontSize: '0.85rem',
                        display: 'block',
                      }}
                    >
                      📦 My Orders
                    </button>

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        navigate('/admin/products');
                      }}
                      style={{
                        width: '100%',
                        textAlign: 'left',
                        padding: '0.5rem',
                        background: 'transparent',
                        color: 'var(--accent-primary)',
                        fontSize: '0.85rem',
                        fontWeight: 600,
                        display: 'block',
                      }}
                    >
                      🛍️ Manage Products
                    </button>

                    {isManager && (
                      <button
                        onClick={() => {
                          setDropdownOpen(false);
                          navigate('/admin/dashboard');
                        }}
                        style={{
                          width: '100%',
                          textAlign: 'left',
                          padding: '0.5rem',
                          background: 'transparent',
                          color: 'var(--text-secondary)',
                          fontSize: '0.85rem',
                          fontWeight: 500,
                          display: 'block',
                        }}
                      >
                        📊 Admin Dashboard
                      </button>
                    )}

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        logout();
                        navigate('/login');
                      }}
                      style={{
                        width: '100%',
                        textAlign: 'left',
                        padding: '0.5rem',
                        background: 'transparent',
                        color: 'var(--accent-rose)',
                        fontSize: '0.85rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.4rem',
                        marginTop: '0.25rem',
                      }}
                    >
                      <LogOut size={14} /> Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <Link
                  to="/login"
                  style={{
                    padding: '0.45rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)',
                    fontSize: '0.9rem',
                    fontWeight: 500,
                  }}
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  style={{
                    padding: '0.45rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    background: 'var(--accent-primary)',
                    color: '#fff',
                    fontSize: '0.9rem',
                    fontWeight: 600,
                  }}
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* RAG Search Modal */}
      <RAGSearchModal isOpen={isRAGOpen} onClose={() => setIsRAGOpen(false)} />
    </>
  );
};
