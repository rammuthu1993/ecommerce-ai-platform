import { apiRequest } from './api';
import { InventoryItem, ApiResponse } from '../types';

export const inventoryService = {
  getInventory: () => apiRequest<ApiResponse<InventoryItem[]>>('/api/inventory'),
  adjustStock: (payload: { product_id: number; quantity_delta: number; tx_type?: string }) =>
    apiRequest<ApiResponse<InventoryItem>>('/api/inventory/adjust', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getLowStock: (threshold = 5) => apiRequest<ApiResponse<InventoryItem[]>>(`/api/inventory/low-stock?threshold=${threshold}`),
  getOutOfStock: () => apiRequest<ApiResponse<InventoryItem[]>>('/api/inventory/out-of-stock'),
};
