import React, { useEffect, useState } from 'react';
import { Warehouse, AlertTriangle, CheckCircle } from 'lucide-react';
import { inventoryService } from '../services/inventoryService';
import { InventoryItem } from '../types';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

export const InventoryPage: React.FC = () => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [filter, setFilter] = useState<'all' | 'low' | 'out'>('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);
  const [delta, setDelta] = useState<string>('5');

  const loadData = () => {
    if (filter === 'low') {
      inventoryService.getLowStock().then((res) => setItems(res.data)).catch(() => {});
    } else if (filter === 'out') {
      inventoryService.getOutOfStock().then((res) => setItems(res.data)).catch(() => {});
    } else {
      inventoryService.getInventory().then((res) => setItems(res.data)).catch(() => {});
    }
  };

  useEffect(() => {
    loadData();
  }, [filter]);

  const handleOpenAdjust = (prodId: number) => {
    setSelectedProductId(prodId);
    setDelta('5');
    setIsModalOpen(true);
  };

  const handleAdjustSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedProductId) return;

    await inventoryService.adjustStock({
      product_id: selectedProductId,
      quantity_delta: parseInt(delta),
    });

    setIsModalOpen(false);
    loadData();
  };

  return (
    <div style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800 }}>Inventory & Stock Management</h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Track stock levels, reservations, and reorders</p>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={() => setFilter('all')}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: filter === 'all' ? 'var(--accent-primary)' : 'rgba(255,255,255,0.05)',
              color: '#fff',
              fontWeight: 500,
              fontSize: '0.85rem',
            }}
          >
            All Stock
          </button>
          <button
            onClick={() => setFilter('low')}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: filter === 'low' ? 'var(--accent-amber)' : 'rgba(255,255,255,0.05)',
              color: '#fff',
              fontWeight: 500,
              fontSize: '0.85rem',
            }}
          >
            Low Stock (&lt;5)
          </button>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '1.25rem' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.75rem' }}>Product</th>
              <th style={{ padding: '0.75rem' }}>Location</th>
              <th style={{ padding: '0.75rem' }}>Stock Quantity</th>
              <th style={{ padding: '0.75rem' }}>Reserved</th>
              <th style={{ padding: '0.75rem' }}>Available</th>
              <th style={{ padding: '0.75rem' }}>Status</th>
              <th style={{ padding: '0.75rem', textAlign: 'right' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '0.75rem', fontWeight: 600 }}>{item.product_name}</td>
                <td style={{ padding: '0.75rem', color: 'var(--text-secondary)' }}>{item.location}</td>
                <td style={{ padding: '0.75rem', fontWeight: 600 }}>{item.stock_quantity}</td>
                <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>{item.reserved_quantity}</td>
                <td style={{ padding: '0.75rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>
                  {item.available_quantity}
                </td>
                <td style={{ padding: '0.75rem' }}>
                  {item.stock_quantity === 0 ? (
                    <Badge variant="danger">Out of Stock</Badge>
                  ) : item.stock_quantity <= 5 ? (
                    <Badge variant="warning">Low Stock</Badge>
                  ) : (
                    <Badge variant="success">In Stock</Badge>
                  )}
                </td>
                <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                  <button
                    onClick={() => handleOpenAdjust(item.product_id)}
                    style={{
                      padding: '0.35rem 0.75rem',
                      borderRadius: 'var(--radius-sm)',
                      background: 'rgba(99,102,241,0.15)',
                      color: 'var(--accent-primary)',
                      fontSize: '0.8rem',
                      fontWeight: 600,
                    }}
                  >
                    Adjust Stock
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Adjust Product Stock">
        <form onSubmit={handleAdjustSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Stock Quantity Delta (+/-)
            </label>
            <input
              type="number"
              required
              value={delta}
              onChange={(e) => setDelta(e.target.value)}
              placeholder="e.g. 10 or -5"
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
              }}
            />
          </div>

          <button
            type="submit"
            style={{
              padding: '0.75rem',
              borderRadius: 'var(--radius-md)',
              background: 'var(--accent-primary)',
              color: '#fff',
              fontWeight: 600,
            }}
          >
            Confirm Adjustment
          </button>
        </form>
      </Modal>
    </div>
  );
};
