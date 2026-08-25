import React, { useEffect, useState } from 'react';
import { Plus, Trash2, FolderTree } from 'lucide-react';
import { categoryService } from '../services/categoryService';
import { Category } from '../types';
import { Modal } from '../components/common/Modal';

export const CategoriesPage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const loadData = () => {
    categoryService.getCategories().then((res) => setCategories(res.data)).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await categoryService.createCategory({ name, description });
    setIsModalOpen(false);
    setName('');
    setDescription('');
    loadData();
  };

  const handleDelete = async (id: number) => {
    if (confirm('Delete category?')) {
      await categoryService.deleteCategory(id);
      loadData();
    }
  };

  return (
    <div style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800 }}>Categories Management</h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Manage store product categories</p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          style={{
            padding: '0.65rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            background: 'var(--accent-primary)',
            color: '#fff',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
          }}
        >
          <Plus size={18} /> Add Category
        </button>
      </div>

      <div className="glass-panel" style={{ padding: '1.25rem' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.75rem' }}>ID</th>
              <th style={{ padding: '0.75rem' }}>Category Name</th>
              <th style={{ padding: '0.75rem' }}>Description</th>
              <th style={{ padding: '0.75rem', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {categories.map((c) => (
              <tr key={c.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '0.75rem' }}>#{c.id}</td>
                <td style={{ padding: '0.75rem', fontWeight: 600 }}>{c.name}</td>
                <td style={{ padding: '0.75rem', color: 'var(--text-secondary)' }}>{c.description || '—'}</td>
                <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                  <button onClick={() => handleDelete(c.id)} style={{ background: 'transparent', color: 'var(--accent-rose)' }}>
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create New Category">
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Category Name
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
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

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Description
            </label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
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
              marginTop: '0.5rem',
            }}
          >
            Create Category
          </button>
        </form>
      </Modal>
    </div>
  );
};
