import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  FolderTree,
  Warehouse,
  Users,
  Truck,
  FileSpreadsheet,
  Bot
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const links = [
    { to: '/admin/dashboard', label: 'Executive Dashboard', icon: <LayoutDashboard size={18} /> },
    { to: '/admin/products', label: 'Products Management', icon: <Package size={18} /> },
    { to: '/admin/categories', label: 'Categories', icon: <FolderTree size={18} /> },
    { to: '/admin/inventory', label: 'Stock & Inventory', icon: <Warehouse size={18} /> },
    { to: '/admin/customers', label: 'Customers', icon: <Users size={18} /> },
    { to: '/admin/suppliers', label: 'Suppliers & Purchases', icon: <Truck size={18} /> },
  ];

  return (
    <aside
      className="glass-panel"
      style={{
        width: '240px',
        minHeight: 'calc(100vh - 70px)',
        padding: '1.25rem 0.85rem',
        borderRadius: 0,
        borderTop: 'none',
        borderBottom: 'none',
        borderLeft: 'none',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
        <span style={{ padding: '0 0.5rem 0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Store Management
        </span>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              padding: '0.65rem 0.85rem',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.9rem',
              fontWeight: 500,
              color: isActive ? '#fff' : 'var(--text-secondary)',
              background: isActive ? 'linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.2))' : 'transparent',
              border: isActive ? '1px solid var(--border-glow)' : '1px solid transparent',
              transition: 'all 0.2s ease',
            })}
          >
            {link.icon}
            <span>{link.label}</span>
          </NavLink>
        ))}
      </div>
    </aside>
  );
};
