import { apiRequest } from './api';
import { Product, ApiResponse } from '../types';

export const productService = {
  getProducts: (params?: { page?: number; limit?: number; search?: string; category_id?: number; min_price?: number; max_price?: number }) => {
    const query = new URLSearchParams();
    if (params?.page) query.append('page', params.page.toString());
    if (params?.limit) query.append('limit', params.limit.toString());
    if (params?.search) query.append('search', params.search);
    if (params?.category_id) query.append('category_id', params.category_id.toString());
    if (params?.min_price) query.append('min_price', params.min_price.toString());
    if (params?.max_price) query.append('max_price', params.max_price.toString());

    return apiRequest<ApiResponse<Product[]>>(`/api/products?${query.toString()}`);
  },

  getProduct: (id: number) => apiRequest<ApiResponse<Product>>(`/api/products/${id}`),

  createProduct: (payload: { name: string; category_id: number; price: number; quantity?: number; description?: string }) =>
    apiRequest<ApiResponse<Product>>('/api/products', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  updateProduct: (id: number, payload: Partial<Product>) =>
    apiRequest<ApiResponse<Product>>(`/api/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),

  deleteProduct: (id: number) =>
    apiRequest<ApiResponse<{ product_id: number }>>(`/api/products/${id}`, {
      method: 'DELETE',
    }),
};
