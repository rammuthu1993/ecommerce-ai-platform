import { apiRequest } from './api';
import { RAGQueryResult, AgentQueryResult, ApiResponse } from '../types';

export const aiService = {
  chat: (prompt: string) =>
    apiRequest<ApiResponse<{ prompt: string; reply: string }>>('/api/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ prompt }),
    }),

  queryRAG: (query: string) =>
    apiRequest<ApiResponse<RAGQueryResult>>('/api/ai/rag/query', {
      method: 'POST',
      body: JSON.stringify({ query }),
    }),

  queryAgent: (query: string, sessionId?: string) =>
    apiRequest<ApiResponse<AgentQueryResult>>('/api/ai/agent/query', {
      method: 'POST',
      body: JSON.stringify({ query, session_id: sessionId }),
    }),

  getKnowledge: () => apiRequest<ApiResponse<any[]>>('/api/ai/knowledge'),
  getTokenUsage: () => apiRequest<ApiResponse<any>>('/api/ai/token-usage'),
  getAgentMetrics: () => apiRequest<ApiResponse<any>>('/api/ai/agent/metrics'),
};
