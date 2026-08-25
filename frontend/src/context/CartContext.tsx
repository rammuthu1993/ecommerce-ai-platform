import React, { createContext, useContext, useState, useEffect } from 'react';
import { CartItem, Product } from '../types';
import { useAuth } from './AuthContext';
import { orderService } from '../services/orderService';

interface CartContextType {
  cartItems: CartItem[];
  subtotal: number;
  itemCount: number;
  addToCart: (product: Product, quantity?: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  removeFromCart: (productId: number) => void;
  clearCart: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [cartItems, setCartItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem('local_cart');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('local_cart', JSON.stringify(cartItems));
  }, [cartItems]);

  useEffect(() => {
    if (user) {
      orderService
        .getCart(user.id)
        .then((res) => {
          if (res.data?.items) {
            setCartItems(res.data.items);
          }
        })
        .catch(() => {});
    }
  }, [user]);

  const addToCart = (product: Product, quantity = 1) => {
    setCartItems((prev) => {
      const existingIndex = prev.findIndex((item) => item.product_id === product.id);
      if (existingIndex > -1) {
        const updated = [...prev];
        const newQty = updated[existingIndex].quantity + quantity;
        updated[existingIndex] = {
          ...updated[existingIndex],
          quantity: newQty,
          line_total: newQty * updated[existingIndex].unit_price,
        };
        return updated;
      }
      return [
        ...prev,
        {
          product_id: product.id,
          product_name: product.name,
          unit_price: product.price,
          quantity,
          line_total: product.price * quantity,
        },
      ];
    });

    if (user) {
      orderService.addToCart(user.id, product.id, quantity).catch(() => {});
    }
  };

  const updateQuantity = (productId: number, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(productId);
      return;
    }
    setCartItems((prev) =>
      prev.map((item) =>
        item.product_id === productId
          ? { ...item, quantity, line_total: quantity * item.unit_price }
          : item
      )
    );
    if (user) {
      orderService.updateCartItem(user.id, productId, quantity).catch(() => {});
    }
  };

  const removeFromCart = (productId: number) => {
    setCartItems((prev) => prev.filter((item) => item.product_id !== productId));
    if (user) {
      orderService.removeFromCart(user.id, productId).catch(() => {});
    }
  };

  const clearCart = () => {
    setCartItems([]);
    if (user) {
      orderService.clearCart(user.id).catch(() => {});
    }
  };

  const subtotal = cartItems.reduce((sum, item) => sum + item.line_total, 0);
  const itemCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        cartItems,
        subtotal,
        itemCount,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within a CartProvider');
  return context;
};
