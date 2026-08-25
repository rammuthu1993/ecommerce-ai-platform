import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Package, ShoppingBag, Plus, CheckCircle, Edit, Trash2 } from 'lucide-react';
import { productService } from '../services/productService';
import { categoryService } from '../services/categoryService';
import { Product, Category } from '../types';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { Modal } from '../components/common/Modal';

export const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
  const [minPrice, setMinPrice] = useState<string>('');
  const [maxPrice, setMaxPrice] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [addedToast, setAddedToast] = useState<string | null>(null);
  const [crudMessage, setCrudMessage] = useState<string | null>(null);
  const [crudError, setCrudError] = useState<string | null>(null);

  // CRUD Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [name, setName] = useState('');
  const [categoryId, setCategoryId] = useState<number>(1);
  const [price, setPrice] = useState<string>('');
  const [quantity, setQuantity] = useState<string>('10');

  const { addToCart } = useCart();
  const { isManager, isAuthenticated } = useAuth();

  const fetchProducts = () => {
    setIsLoading(true);
    productService
      .getProducts({
        search: search || undefined,
        category_id: selectedCategory,
        min_price: minPrice ? parseFloat(minPrice) : undefined,
        max_price: maxPrice ? parseFloat(maxPrice) : undefined,
      })
      .then((res) => setProducts(res.data))
      .catch(() => {})
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    categoryService.getCategories().then((res) => setCategories(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [selectedCategory]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchProducts();
  };

  const handleAddToCart = (prod: Product) => {
    addToCart(prod, 1);
    setAddedToast(`Added "${prod.name}" to cart!`);
    setTimeout(() => setAddedToast(null), 3000);
  };

  const handleOpenCreate = () => {
    setEditingProduct(null);
    setName('');
    setPrice('');
    setQuantity('10');
    if (categories.length > 0) setCategoryId(categories[0].id);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (prod: Product) => {
    setEditingProduct(prod);
    setName(prod.name);
    setCategoryId(prod.category_id || 1);
    setPrice(prod.price.toString());
    setQuantity((prod.quantity || 10).toString());
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this product?')) {
      try {
        await productService.deleteProduct(id);
        setCrudMessage('Product deleted successfully.');
        fetchProducts();
      } catch (err: any) {
        setCrudError(err.message || 'Unable to delete the product.');
      }
    }
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
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
        setCrudMessage('Product updated successfully.');
      } else {
        await productService.createProduct(payload);
        setCrudMessage('Product added successfully.');
      }
      setCrudError(null);
      setIsModalOpen(false);
      fetchProducts();
    } catch (err: any) {
      setCrudError(err.message || 'Unable to save the product.');
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      {/* Added to Cart Notification Toast */}
      {addedToast && (
        <div
          className="animate-fade-in"
          style={{
            position: 'fixed',
            bottom: '24px',
            left: '24px',
            zIndex: 999,
            padding: '0.85rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            background: 'linear-gradient(135deg, #10b981, #059669)',
            color: '#fff',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            boxShadow: 'var(--shadow-glow)',
          }}
        >
          <CheckCircle size={20} /> {addedToast}
        </div>
      )}
      {(crudMessage || crudError) && (
        <div className="animate-fade-in" style={{ marginBottom: '1rem', padding: '0.85rem 1rem', borderRadius: 'var(--radius-md)', background: crudError ? 'rgba(244, 63, 94, 0.15)' : 'rgba(16, 185, 129, 0.15)', color: crudError ? 'var(--accent-rose)' : 'var(--accent-emerald)', border: '1px solid currentColor' }}>
          {crudError || crudMessage}
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800 }}>Store Catalog</h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Explore high-quality products with real-time stock status
          </p>
        </div>

        {/* Add Product Button (Visible when logged in or admin/manager) */}
        {(isAuthenticated || isManager) && (
          <button
            onClick={handleOpenCreate}
            style={{
              padding: '0.75rem 1.35rem',
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: '#fff',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              boxShadow: 'var(--shadow-glow)',
            }}
          >
            <Plus size={20} /> Add New Product
          </button>
        )}
      </div>

      {/* Filter & Search Bar */}
      <form
        onSubmit={handleSearchSubmit}
        className="glass-panel"
        style={{
          padding: '1.25rem',
          marginBottom: '2rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '1rem',
          alignItems: 'end',
        }}
      >
        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
            Search Products
          </label>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search laptop, phone..."
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
            value={selectedCategory || ''}
            onChange={(e) => setSelectedCategory(e.target.value ? parseInt(e.target.value) : undefined)}
            style={{
              width: '100%',
              padding: '0.65rem 0.85rem',
              borderRadius: 'var(--radius-md)',
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
            }}
          >
            <option value="">All Categories</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
            Min Price ($)
          </label>
          <input
            type="number"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="0"
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
            Max Price ($)
          </label>
          <input
            type="number"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="10000"
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
            padding: '0.65rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            background: 'var(--accent-primary)',
            color: '#fff',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.4rem',
          }}
        >
          <Filter size={16} /> Filter
        </button>
      </form>

      {/* Product Cards Grid */}
      {isLoading ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>Loading catalog...</div>
      ) : products.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>No products found matching filters.</div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '1.5rem' }}>
          {products.map((prod) => (
            <div key={prod.id} className="glass-panel glass-panel-hover" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', position: 'relative' }}>
              {/* Product Edit / Delete Actions on Card (Available After Login) */}
              {(isAuthenticated || isManager) && (
                <div style={{ position: 'absolute', top: '12px', right: '12px', display: 'flex', gap: '0.35rem' }}>
                  <button
                    onClick={() => handleOpenEdit(prod)}
                    style={{
                      padding: '0.35rem',
                      borderRadius: 'var(--radius-sm)',
                      background: 'rgba(99, 102, 241, 0.2)',
                      color: 'var(--accent-primary)',
                    }}
                  >
                    <Edit size={14} />
                  </button>
                  <button
                    onClick={() => handleDelete(prod.id)}
                    style={{
                      padding: '0.35rem',
                      borderRadius: 'var(--radius-sm)',
                      background: 'rgba(244, 63, 94, 0.2)',
                      color: 'var(--accent-rose)',
                    }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              )}

              <div
                style={{
                  height: '160px',
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
              <p style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--accent-emerald)', marginBottom: '1rem' }}>
                ${prod.price.toFixed(2)}
              </p>
              <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto' }}>
                <Link
                  to={`/products/${prod.id}`}
                  style={{
                    flex: 1,
                    padding: '0.65rem',
                    borderRadius: 'var(--radius-md)',
                    background: 'rgba(255, 255, 255, 0.08)',
                    color: 'var(--text-primary)',
                    textAlign: 'center',
                    fontWeight: 600,
                    fontSize: '0.85rem',
                  }}
                >
                  Details
                </Link>
                <button
                  onClick={() => handleAddToCart(prod)}
                  style={{
                    padding: '0.65rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    background: 'var(--accent-primary)',
                    color: '#fff',
                    fontWeight: 600,
                    fontSize: '0.85rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                  }}
                >
                  <ShoppingBag size={16} /> Add
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Product Create / Edit Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingProduct ? 'Edit Product' : 'Add New Product'}>
        <form onSubmit={handleFormSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
              Product Name
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Wireless Gaming Mouse"
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
              placeholder="49.99"
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
              Initial Quantity
            </label>
            <input
              type="number"
              required
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder="10"
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
            {editingProduct ? 'Save Changes' : 'Create Product'}
          </button>
        </form>
      </Modal>
    </div>
  );
};
