import { apiRequest } from './api';
import { ExecutiveKPIs, ApiResponse } from '../types';

export const analyticsService = {
  getKPIs: () => apiRequest<ApiResponse<ExecutiveKPIs>>('/api/analytics/kpis'),
  getSalesTrend: (freq = 'D') => apiRequest<ApiResponse<any[]>>(`/api/analytics/sales-trend?freq=${freq}`),
  getSalesByGroup: (by = 'category') => apiRequest<ApiResponse<any[]>>(`/api/analytics/groupby?by=${by}`),
  getRFMSegmentation: () => apiRequest<ApiResponse<any[]>>('/api/analytics/rfm-segmentation'),
  getNumpyBenchmark: (items = 100000) => apiRequest<ApiResponse<any>>(`/api/analytics/numpy-benchmark?items=${items}`),
  getDemandOptimization: (basePrice = 1000) => apiRequest<ApiResponse<any>>(`/api/analytics/demand-optimization?base_price=${basePrice}`),
  getExportUrl: (dataset = 'sales', format = 'csv') => `/api/analytics/export?dataset=${dataset}&format=${format}`,
};
