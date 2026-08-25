import { apiRequest } from './api';
import { Cart, Order, ApiResponse } from '../types';

export const orderService = {
  getCart: (customerId: number) => apiRequest<ApiResponse<Cart>>(`/api/cart/${customerId}`),
  addToCart: (customerId: number, productId: number, quantity: number) =>
    apiRequest<ApiResponse<Cart>>(`/api/cart/${customerId}/items`, {
      method: 'POST',
      body: JSON.stringify({ product_id: productId, quantity }),
    }),
  updateCartItem: (customerId: number, productId: number, quantity: number) =>
    apiRequest<ApiResponse<Cart>>(`/api/cart/${customerId}/items`, {
      method: 'PUT',
      body: JSON.stringify({ product_id: productId, quantity }),
    }),
  removeFromCart: (customerId: number, productId: number) =>
    apiRequest<ApiResponse<Cart>>(`/api/cart/${customerId}/items/${productId}`, {
      method: 'DELETE',
    }),
  clearCart: (customerId: number) =>
    apiRequest<ApiResponse<Cart>>(`/api/cart/${customerId}`, {
      method: 'DELETE',
    }),
  checkout: (payload: { customer_id: number; shipping_address_id?: number }) =>
    apiRequest<ApiResponse<Order>>('/api/orders/checkout', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getOrders: (params?: { customer_id?: number; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.customer_id) query.append('customer_id', params.customer_id.toString());
    if (params?.status) query.append('status', params.status);
    return apiRequest<ApiResponse<Order[]>>(`/api/orders?${query.toString()}`);
  },
  getOrder: (id: number) => apiRequest<ApiResponse<Order>>(`/api/orders/${id}`),
  updateOrderStatus: (id: number, status: string) =>
    apiRequest<ApiResponse<Order>>(`/api/orders/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    }),
  getInvoice: (orderId: number) => apiRequest<ApiResponse<any>>(`/api/invoices/${orderId}`),
};
