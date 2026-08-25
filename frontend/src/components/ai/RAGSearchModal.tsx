import React, { useState } from 'react';
import { Search, BookOpen, ExternalLink } from 'lucide-react';
import { Modal } from '../common/Modal';
import { aiService } from '../../services/aiService';
import { RAGQueryResult } from '../../types';

interface RAGSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const RAGSearchModal: React.FC<RAGSearchModalProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<RAGQueryResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setIsLoading(true);
    try {
      const res = await aiService.queryRAG(query);
      setResult(res.data);
    } catch (err: any) {
      alert(`Error searching RAG knowledge base: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Store Policy Knowledge Base Search">
      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. What is the return refund policy?"
          style={{
            flex: 1,
            padding: '0.65rem 0.85rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-primary)',
            outline: 'none',
          }}
        />
        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: '0.65rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            background: 'var(--accent-primary)',
            color: '#fff',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
          }}
        >
          <Search size={16} /> Search
        </button>
      </form>

      {isLoading && (
        <div style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--text-muted)' }}>
          Retrieving TF-IDF vector chunks & generating grounded response...
        </div>
      )}

      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div
            style={{
              padding: '1rem',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(99, 102, 241, 0.1)',
              border: '1px solid var(--border-glow)',
            }}
          >
            <h4 style={{ fontSize: '0.9rem', color: 'var(--accent-primary)', marginBottom: '0.5rem', fontWeight: 600 }}>
              Grounded AI Response:
            </h4>
            <p style={{ fontSize: '0.9rem', lineHeight: 1.6 }}>{result.answer}</p>
          </div>

          {result.sources && result.sources.length > 0 && (
            <div>
              <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
                Cited Document Sources:
              </h5>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {result.sources.map((s, idx) => (
                  <span
                    key={idx}
                    style={{
                      padding: '0.25rem 0.65rem',
                      borderRadius: 'var(--radius-full)',
                      background: 'rgba(255, 255, 255, 0.08)',
                      fontSize: '0.75rem',
                      color: 'var(--accent-emerald)',
                      border: '1px solid var(--border-color)',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                    }}
                  >
                    <BookOpen size={12} /> {s}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </Modal>
  );
};
