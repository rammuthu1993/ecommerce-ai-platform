import React, { useEffect, useState } from 'react';
import { apiRequest } from '../services/api';
import { Supplier, PurchaseOrder, ApiResponse } from '../types';
import { Badge } from '../components/common/Badge';

export const SuppliersPurchasesPage: React.FC = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [purchases, setPurchases] = useState<PurchaseOrder[]>([]);

  useEffect(() => {
    apiRequest<ApiResponse<Supplier[]>>('/api/suppliers').then((res) => setSuppliers(res.data)).catch(() => {});
    apiRequest<ApiResponse<PurchaseOrder[]>>('/api/purchases').then((res) => setPurchases(res.data)).catch(() => {});
  }, []);

  return (
    <div style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.25rem' }}>Suppliers & Purchase Orders</h1>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Vendor management and replenishment procurement
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1rem' }}>Supplier Directory</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '0.65rem' }}>ID</th>
                <th style={{ padding: '0.65rem' }}>Supplier</th>
                <th style={{ padding: '0.65rem' }}>Contact</th>
                <th style={{ padding: '0.65rem' }}>Email</th>
              </tr>
            </thead>
            <tbody>
              {suppliers.map((s) => (
                <tr key={s.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '0.65rem' }}>#{s.id}</td>
                  <td style={{ padding: '0.65rem', fontWeight: 600 }}>{s.name}</td>
                  <td style={{ padding: '0.65rem' }}>{s.contact_name || '—'}</td>
                  <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>{s.email || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1rem' }}>Purchase Orders</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '0.65rem' }}>PO ID</th>
                <th style={{ padding: '0.65rem' }}>Supplier</th>
                <th style={{ padding: '0.65rem' }}>Total ($)</th>
                <th style={{ padding: '0.65rem' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {purchases.map((po) => (
                <tr key={po.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '0.65rem' }}>#{po.id}</td>
                  <td style={{ padding: '0.65rem', fontWeight: 600 }}>Supplier #{po.supplier_id}</td>
                  <td style={{ padding: '0.65rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>
                    ${po.total_amount.toFixed(2)}
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    <Badge variant={po.status === 'RECEIVED' ? 'success' : 'warning'}>{po.status}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
