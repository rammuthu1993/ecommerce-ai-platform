import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { Footer } from './components/layout/Footer';
import { AIAssistantWidget } from './components/ai/AIAssistantWidget';

import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { ProductsPage } from './pages/ProductsPage';
import { ProductDetailPage } from './pages/ProductDetailPage';
import { AdminProductsPage } from './pages/AdminProductsPage';
import { CategoriesPage } from './pages/CategoriesPage';
import { InventoryPage } from './pages/InventoryPage';
import { CustomersPage } from './pages/CustomersPage';
import { SuppliersPurchasesPage } from './pages/SuppliersPurchasesPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { OrdersPage } from './pages/OrdersPage';
import { InvoicePage } from './pages/InvoicePage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { NotFoundPage } from './pages/NotFoundPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode; requireAdmin?: boolean }> = ({
  children,
  requireAdmin = false,
}) => {
  const { isAuthenticated, isManager, isLoading } = useAuth();

  if (isLoading) return <div style={{ padding: '4rem', textAlign: 'center' }}>Authenticating...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (requireAdmin && !isManager) return <Navigate to="/" replace />;

  return <>{children}</>;
};

const AdminLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div style={{ display: 'flex', minHeight: 'calc(100vh - 70px)' }}>
      <Sidebar />
      <main style={{ flex: 1, padding: '1.5rem', width: '100%', overflowX: 'hidden' }}>{children}</main>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Navbar />
            <div style={{ flex: 1 }}>
              <Routes>
                {/* Public Store Routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/products" element={<ProductsPage />} />
                <Route path="/products/:id" element={<ProductDetailPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/checkout" element={<CheckoutPage />} />
                <Route path="/orders" element={<OrdersPage />} />
                <Route path="/invoices/:orderId" element={<InvoicePage />} />

                {/* Protected Admin Routes */}
                <Route
                  path="/admin/dashboard"
                  element={
                    <ProtectedRoute requireAdmin>
                      <AdminLayout>
                        <AdminDashboardPage />
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/products"
                  element={
                    <ProtectedRoute>
                      <AdminLayout>
                        <AdminProductsPage />
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/categories"
                  element={
                    <ProtectedRoute requireAdmin>
                      <AdminLayout>
                        <CategoriesPage />
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/inventory"
                  element={
                    <ProtectedRoute requireAdmin>
                      <AdminLayout>
                        <InventoryPage />
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/customers"
                  element={
                    <ProtectedRoute requireAdmin>
                      <AdminLayout>
                        <CustomersPage />
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/suppliers"
                  element={
                    <ProtectedRoute requireAdmin>
                      <AdminLayout>
                        <SuppliersPurchasesPage />
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />

                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </div>
            <Footer />
            {/* Floating AI Business Assistant Chatbot Widget */}
            <AIAssistantWidget />
          </div>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
};
