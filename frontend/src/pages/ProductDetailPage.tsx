import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Package, ShoppingBag, ArrowLeft, ShieldCheck, Truck, Edit, Trash2 } from 'lucide-react';
import { productService } from '../services/productService';
import { categoryService } from '../services/categoryService';
import { Product, Category } from '../types';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { Modal } from '../components/common/Modal';

export const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Edit Modal State
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editName, setEditName] = useState('');
  const [editCategoryId, setEditCategoryId] = useState<number>(1);
  const [editPrice, setEditPrice] = useState<string>('');
  const [editQuantity, setEditQuantity] = useState<string>('10');

  const { addToCart } = useCart();
  const { isAuthenticated, isManager } = useAuth();

  const loadProduct = () => {
    if (id) {
      setIsLoading(true);
      productService
        .getProduct(parseInt(id))
        .then((res) => setProduct(res.data))
        .catch(() => {})
        .finally(() => setIsLoading(false));
    }
  };

  useEffect(() => {
    loadProduct();
    categoryService.getCategories().then((res) => setCategories(res.data)).catch(() => {});
  }, [id]);

  const handleOpenEdit = () => {
    if (!product) return;
    setEditName(product.name);
    setEditCategoryId(product.category_id || 1);
    setEditPrice(product.price.toString());
    setEditQuantity((product.quantity || 10).toString());
    setIsEditModalOpen(true);
  };

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!product) return;

    try {
      await productService.updateProduct(product.id, {
        name: editName,
        category_id: editCategoryId,
        price: parseFloat(editPrice),
        quantity: parseInt(editQuantity),
      });
      setFeedback('Product updated successfully!');
      setError(null);
      setIsEditModalOpen(false);
      loadProduct();
    } catch (err: any) {
      setError(err.message || 'Failed to update product.');
    }
  };

  const handleDelete = async () => {
    if (!product) return;
    if (confirm(`Are you sure you want to delete "${product.name}"?`)) {
      try {
        await productService.deleteProduct(product.id);
        navigate('/products');
      } catch (err: any) {
        setError(err.message || 'Failed to delete product.');
      }
    }
  };

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Loading product details...</div>;
  if (!product) return <div style={{ padding: '4rem', textAlign: 'center' }}>Product not found.</div>;

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <Link
          to="/products"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)' }}
        >
          <ArrowLeft size={16} /> Back to Catalog
        </Link>

        {/* Update & Delete Options (Available After Login) */}
        {(isAuthenticated || isManager) && (
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={handleOpenEdit}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(99, 102, 241, 0.2)',
                color: 'var(--accent-primary)',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem',
                fontSize: '0.85rem',
                border: '1px solid rgba(99, 102, 241, 0.3)',
              }}
            >
              <Edit size={16} /> Edit Product
            </button>
            <button
              onClick={handleDelete}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(244, 63, 94, 0.2)',
                color: 'var(--accent-rose)',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem',
                fontSize: '0.85rem',
                border: '1px solid rgba(244, 63, 94, 0.3)',
              }}
            >
              <Trash2 size={16} /> Delete Product
            </button>
          </div>
        )}
      </div>

      {(feedback || error) && (
        <div className="animate-fade-in" style={{ marginBottom: '1rem', padding: '0.85rem 1rem', borderRadius: 'var(--radius-md)', background: error ? 'rgba(244, 63, 94, 0.15)' : 'rgba(16, 185, 129, 0.15)', color: error ? 'var(--accent-rose)' : 'var(--accent-emerald)', border: '1px solid currentColor' }}>
          {error || feedback}
        </div>
      )}

      <div
        className="glass-panel"
        style={{
          padding: '2.5rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '2.5rem',
        }}
      >
        {/* Product Image Box */}
        <div
          style={{
            height: '320px',
            borderRadius: 'var(--radius-lg)',
            background: 'rgba(255, 255, 255, 0.03)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-primary)',
          }}
        >
          <Package size={96} />
        </div>

        {/* Product Information */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--accent-primary)', fontWeight: 600, textTransform: 'uppercase' }}>
            Category ID: #{product.category_id}
          </span>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800, marginTop: '0.25rem', marginBottom: '0.75rem' }}>{product.name}</h1>
          <p style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-emerald)', marginBottom: '1.5rem' }}>
            ${product.price.toFixed(2)}
          </p>

          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '2rem' }}>
            High-grade ecommerce product with real-time stock allocation and automated purchase order sync.
          </p>

          {/* Quantity Selector & Add to Cart */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)' }}>
              <button
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                style={{ padding: '0.65rem 1rem', background: 'transparent', color: 'var(--text-primary)' }}
              >
                -
              </button>
              <span style={{ padding: '0 1rem', fontWeight: 600 }}>{quantity}</span>
              <button
                onClick={() => setQuantity((q) => q + 1)}
                style={{ padding: '0.65rem 1rem', background: 'transparent', color: 'var(--text-primary)' }}
              >
                +
              </button>
            </div>

            <button
              onClick={() => addToCart(product, quantity)}
              style={{
                flex: 1,
                padding: '0.85rem 1.5rem',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                color: '#fff',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
              }}
            >
              <ShoppingBag size={18} /> Add to Shopping Cart
            </button>
          </div>

          <div style={{ display: 'flex', gap: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Truck size={16} /> Free Shipping Over $50
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <ShieldCheck size={16} /> 100% Quality Guarantee
            </div>
          </div>
        </div>
      </div>

      {/* Product Edit Modal */}
      <Modal isOpen={isEditModalOpen} onClose={() => setIsEditModalOpen(false)} title="Edit Product">
        <form onSubmit={handleEditSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Product Name
            </label>
            <input
              type="text"
              required
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.05)',
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
              value={editCategoryId}
              onChange={(e) => setEditCategoryId(parseInt(e.target.value))}
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
              value={editPrice}
              onChange={(e) => setEditPrice(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Quantity
            </label>
            <input
              type="number"
              required
              value={editQuantity}
              onChange={(e) => setEditQuantity(e.target.value)}
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.05)',
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
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: '#fff',
              fontWeight: 700,
              marginTop: '0.5rem',
            }}
          >
            Save Product Changes
          </button>
        </form>
      </Modal>
    </div>
  );
};

