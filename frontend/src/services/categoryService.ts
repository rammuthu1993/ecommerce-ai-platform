import { apiRequest } from './api';
import { Category, ApiResponse } from '../types';

export const categoryService = {
  getCategories: () => apiRequest<ApiResponse<Category[]>>('/api/categories'),
  getCategory: (id: number) => apiRequest<ApiResponse<Category>>(`/api/categories/${id}`),
  createCategory: (payload: { name: string; description?: string }) =>
    apiRequest<ApiResponse<Category>>('/api/categories', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  updateCategory: (id: number, payload: { name: string; description?: string }) =>
    apiRequest<ApiResponse<Category>>(`/api/categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
  deleteCategory: (id: number) =>
    apiRequest<ApiResponse<{ category_id: number }>>(`/api/categories/${id}`, {
      method: 'DELETE',
    }),
};
