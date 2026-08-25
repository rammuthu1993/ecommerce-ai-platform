import React, { useEffect, useState } from 'react';
import { Plus, Edit, Trash2, Package } from 'lucide-react';
import { productService } from '../services/productService';
import { categoryService } from '../services/categoryService';
import { Product, Category } from '../types';
import { Modal } from '../components/common/Modal';

export const AdminProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  const [name, setName] = useState('');
  const [categoryId, setCategoryId] = useState<number>(1);
  const [price, setPrice] = useState<string>('');
  const [quantity, setQuantity] = useState<string>('10');
  const [feedback, setFeedback] = useState<string | null>(null);

  const loadData = () => {
    productService.getProducts().then((res) => setProducts(res.data)).catch(() => {});
    categoryService.getCategories().then((res) => setCategories(res.data)).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenCreate = () => {
    setEditingProduct(null);
    setName('');
    setPrice('');
    setQuantity('10');
    setIsModalOpen(true);
  };

  const handleOpenEdit = (prod: Product) => {
    setEditingProduct(prod);
    setName(prod.name);
    setCategoryId(prod.category_id);
    setPrice(prod.price.toString());
    setQuantity((prod.quantity || 10).toString());
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this product?')) {
      try {
        await productService.deleteProduct(id);
        setFeedback('Product deleted successfully.');
        loadData();
      } catch (err: any) {
        setFeedback(err.message || 'Unable to delete the product.');
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      name,
      category_id: categoryId,
      price: parseFloat(price),
      quantity: parseInt(quantity),
    };

    try {
      if (editingProduct) {
        await productService.updateProduct(editingProduct.id, payload);
        setFeedback('Product updated successfully.');
      } else {
        await productService.createProduct(payload);
        setFeedback('Product added successfully.');
      }
      setIsModalOpen(false);
      loadData();
    } catch (err: any) {
      setFeedback(err.message || 'Unable to save the product.');
    }
  };

  return (
    <div style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      {feedback && (
        <div className="animate-fade-in" style={{ marginBottom: '1rem', padding: '0.85rem 1rem', borderRadius: 'var(--radius-md)', background: 'rgba(16, 185, 129, 0.15)', color: 'var(--accent-emerald)', border: '1px solid currentColor' }}>
          {feedback}
        </div>
      )}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800 }}>Product Management</h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Manage store product catalog and price updates
          </p>
        </div>

        <button
          onClick={handleOpenCreate}
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
          <Plus size={18} /> Add New Product
        </button>
      </div>

      <div className="glass-panel" style={{ padding: '1.25rem' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.75rem' }}>ID</th>
              <th style={{ padding: '0.75rem' }}>Product Name</th>
              <th style={{ padding: '0.75rem' }}>Category ID</th>
              <th style={{ padding: '0.75rem' }}>Price ($)</th>
              <th style={{ padding: '0.75rem', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((prod) => (
              <tr key={prod.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '0.75rem' }}>#{prod.id}</td>
                <td style={{ padding: '0.75rem', fontWeight: 600 }}>{prod.name}</td>
                <td style={{ padding: '0.75rem' }}>#{prod.category_id}</td>
                <td style={{ padding: '0.75rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>
                  ${prod.price.toFixed(2)}
                </td>
                <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                  <button
                    onClick={() => handleOpenEdit(prod)}
                    style={{ background: 'transparent', color: 'var(--accent-primary)', marginRight: '0.75rem' }}
                  >
                    <Edit size={16} />
                  </button>
                  <button onClick={() => handleDelete(prod.id)} style={{ background: 'transparent', color: 'var(--accent-rose)' }}>
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal Form */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingProduct ? 'Edit Product' : 'Create Product'}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Product Name
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
              Category
            </label>
            <select
              value={categoryId}
              onChange={(e) => setCategoryId(parseInt(e.target.value))}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-md)',
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
              }}
            >
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Price ($)
            </label>
            <input
              type="number"
              step="0.01"
              required
              value={price}
              onChange={(e) => setPrice(e.target.value)}
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
            {editingProduct ? 'Save Changes' : 'Create Product'}
          </button>
        </form>
      </Modal>
    </div>
  );
};
