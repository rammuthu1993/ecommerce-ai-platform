import React, { useEffect, useState } from 'react';
import { DollarSign, ShoppingBag, Users, Warehouse, TrendingUp, Download, Sparkles, Cpu, Search, FileSpreadsheet } from 'lucide-react';
import { analyticsService } from '../services/analyticsService';
import { ExecutiveKPIs } from '../types';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { RAGSearchModal } from '../components/ai/RAGSearchModal';
import { apiRequest } from '../services/api';

export const AdminDashboardPage: React.FC = () => {
  const [kpis, setKPIs] = useState<ExecutiveKPIs | null>(null);
  const [salesTrend, setSalesTrend] = useState<any[]>([]);
  const [rfmSegments, setRfmSegments] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Verification state for NumPy, Pandas & RAG
  const [numpyResult, setNumpyResult] = useState<any | null>(null);
  const [isNumpyLoading, setIsNumpyLoading] = useState(false);
  const [isRAGOpen, setIsRAGOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      analyticsService.getKPIs(),
      analyticsService.getSalesTrend('D'),
      analyticsService.getRFMSegmentation(),
    ])
      .then(([kpiRes, trendRes, rfmRes]) => {
        setKPIs(kpiRes.data);
        setSalesTrend(trendRes.data || []);
        setRfmSegments(rfmRes.data || []);
      })
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  const handleRunNumpyBenchmark = async () => {
    setIsNumpyLoading(true);
    try {
      const res = await apiRequest<any>('/api/analytics/numpy-benchmark');
      setNumpyResult(res.data);
    } catch {
    } finally {
      setIsNumpyLoading(false);
    }
  };

  if (isLoading) return <div style={{ padding: '3rem', textAlign: 'center' }}>Loading Executive Dashboard...</div>;

  return (
    <div style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 800 }}>Executive Analytics & Engine Dashboard</h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Real-time business KPIs, NumPy benchmarks, Pandas time-series, and RAG vector search
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <a
            href={analyticsService.getExportUrl('sales', 'csv')}
            download
            style={{
              padding: '0.65rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: 'var(--accent-primary)',
              color: '#fff',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              fontSize: '0.85rem',
            }}
          >
            <Download size={16} /> Pandas CSV Export
          </a>
          <a
            href={analyticsService.getExportUrl('sales', 'excel')}
            download
            style={{
              padding: '0.65rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, #10b981, #059669)',
              color: '#fff',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              fontSize: '0.85rem',
            }}
          >
            <FileSpreadsheet size={16} /> Excel Export
          </a>
        </div>
      </div>

      {/* Engine Verification & Testing Banner */}
      <div
        className="glass-panel"
        style={{
          padding: '1.25rem 1.5rem',
          marginBottom: '2rem',
          background: 'linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1))',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.25rem' }}>
            ⚡ Verification Engine: RAG, NumPy & Pandas
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Check vector policy retrieval, vector array benchmarks, and DataFrame aggregations
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            onClick={() => setIsRAGOpen(true)}
            style={{
              padding: '0.6rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(255,255,255,0.08)',
              color: 'var(--text-primary)',
              fontWeight: 600,
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem',
            }}
          >
            <Search size={16} color="var(--accent-primary)" /> Check RAG Search
          </button>

          <button
            onClick={handleRunNumpyBenchmark}
            disabled={isNumpyLoading}
            style={{
              padding: '0.6rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: '#fff',
              fontWeight: 600,
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem',
            }}
          >
            <Cpu size={16} /> {isNumpyLoading ? 'Benchmarking...' : 'Check NumPy Benchmark'}
          </button>
        </div>
      </div>

      {/* NumPy Result Display */}
      {numpyResult && (
        <div className="glass-panel animate-fade-in" style={{ padding: '1.25rem', marginBottom: '2rem', borderLeft: '4px solid var(--accent-emerald)' }}>
          <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--accent-emerald)' }}>
            NumPy Array Vectorization Benchmark Results ({numpyResult.items_processed} Items)
          </h4>
          <div style={{ display: 'flex', gap: '2rem', fontSize: '0.85rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>NumPy Execution Time:</span>{' '}
              <strong>{(numpyResult.numpy_execution_time_seconds * 1000).toFixed(2)} ms</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Python Loop Time:</span>{' '}
              <strong>{(numpyResult.python_loop_time_seconds * 1000).toFixed(2)} ms</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Speedup:</span>{' '}
              <strong style={{ color: 'var(--accent-emerald)' }}>{numpyResult.speedup_factor}x faster</strong>
            </div>
          </div>
        </div>
      )}

      {/* KPI Cards Grid (Pandas DataFrame Analytics) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        <StatCard
          title="Total Revenue (Pandas)"
          value={`$${(kpis?.total_revenue || 0).toLocaleString()}`}
          trend="+14.2%"
          subtitle="vs previous period"
          icon={<DollarSign size={24} />}
        />
        <StatCard
          title="Total Orders"
          value={kpis?.total_orders || 0}
          subtitle={`AOV: $${(kpis?.average_order_value || 0).toFixed(2)}`}
          icon={<ShoppingBag size={24} />}
        />
        <StatCard
          title="Active Customers"
          value={kpis?.active_customers || 0}
          subtitle={`CLV: $${(kpis?.customer_lifetime_value || 0).toFixed(2)}`}
          icon={<Users size={24} />}
        />
        <StatCard
          title="Inventory Valuation"
          value={`$${(kpis?.inventory_valuation || 0).toLocaleString()}`}
          subtitle={`${kpis?.total_units_sold || 0} units sold`}
          icon={<Warehouse size={24} />}
        />
      </div>

      {/* Sales Trend Table */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <TrendingUp size={18} color="var(--accent-primary)" /> Daily Sales Trend & 7-Day Moving Average (Pandas Resample)
          </h3>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '0.65rem' }}>Date</th>
                  <th style={{ padding: '0.65rem' }}>Orders</th>
                  <th style={{ padding: '0.65rem' }}>Revenue</th>
                  <th style={{ padding: '0.65rem' }}>7D Moving Avg</th>
                </tr>
              </thead>
              <tbody>
                {salesTrend.slice(0, 5).map((row, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '0.65rem' }}>{row.created_at}</td>
                    <td style={{ padding: '0.65rem' }}>{row.total_orders}</td>
                    <td style={{ padding: '0.65rem', fontWeight: 600, color: 'var(--accent-emerald)' }}>
                      ${row.total_revenue}
                    </td>
                    <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>${row.moving_avg_7d || row.total_revenue}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Customer RFM Segments */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={18} color="var(--accent-secondary)" /> Customer RFM Segmentation (Pandas GroupBy)
          </h3>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '0.65rem' }}>Customer</th>
                  <th style={{ padding: '0.65rem' }}>Recency</th>
                  <th style={{ padding: '0.65rem' }}>Monetary</th>
                  <th style={{ padding: '0.65rem' }}>Segment</th>
                </tr>
              </thead>
              <tbody>
                {rfmSegments.slice(0, 5).map((rfm, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '0.65rem', fontWeight: 500 }}>{rfm.customer_name}</td>
                    <td style={{ padding: '0.65rem' }}>{rfm.recency_days} days ago</td>
                    <td style={{ padding: '0.65rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>
                      ${rfm.monetary_value}
                    </td>
                    <td style={{ padding: '0.65rem' }}>
                      <Badge variant={rfm.segment === 'VIP Customer' ? 'warning' : 'primary'}>
                        {rfm.segment}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <RAGSearchModal isOpen={isRAGOpen} onClose={() => setIsRAGOpen(false)} />
    </div>
  );
};
