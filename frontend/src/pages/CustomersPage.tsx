import React, { useEffect, useState } from 'react';
import { apiRequest } from '../services/api';
import { Customer, ApiResponse } from '../types';

export const CustomersPage: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);

  useEffect(() => {
    apiRequest<ApiResponse<Customer[]>>('/api/customers')
      .then((res) => setCustomers(res.data))
      .catch(() => {});
  }, []);

  return (
    <div style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.25rem' }}>Customer Profiles</h1>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Registered store customers and address directories
      </p>

      <div className="glass-panel" style={{ padding: '1.25rem' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.75rem' }}>ID</th>
              <th style={{ padding: '0.75rem' }}>Name</th>
              <th style={{ padding: '0.75rem' }}>Email</th>
              <th style={{ padding: '0.75rem' }}>Phone</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((c) => (
              <tr key={c.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '0.75rem' }}>#{c.id}</td>
                <td style={{ padding: '0.75rem', fontWeight: 600 }}>
                  {c.first_name} {c.last_name}
                </td>
                <td style={{ padding: '0.75rem', color: 'var(--text-secondary)' }}>{c.email}</td>
                <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>{c.phone || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
