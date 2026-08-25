import { apiRequest } from './api';
import { User, ApiResponse } from '../types';

export const authService = {
  register: (payload: { username: string; email: string; password: string; roles?: string[] }) =>
    apiRequest<ApiResponse<{ user: User; access_token: string }>>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  login: (payload: { email: string; password: string }) =>
    apiRequest<ApiResponse<{ user: User; access_token: string }>>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getProfile: () => apiRequest<ApiResponse<User>>('/api/auth/me'),

  changePassword: (payload: { old_password: string; new_password: string }) =>
    apiRequest<ApiResponse<{ success: boolean }>>('/api/auth/password', {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
};
