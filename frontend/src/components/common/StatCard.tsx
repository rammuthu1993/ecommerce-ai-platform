import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: string;
  glowColor?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
}) => {
  return (
    <div
      className="glass-panel glass-panel-hover"
      style={{
        padding: '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
            {title}
          </span>
          <h3
            style={{
              fontSize: '1.75rem',
              fontWeight: 700,
              marginTop: '0.35rem',
              fontFamily: 'var(--font-heading)',
            }}
          >
            {value}
          </h3>
        </div>
        {icon && (
          <div
            style={{
              padding: '0.75rem',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(99, 102, 241, 0.15)',
              color: 'var(--accent-primary)',
            }}
          >
            {icon}
          </div>
        )}
      </div>
      {(subtitle || trend) && (
        <div
          style={{
            marginTop: '1rem',
            paddingTop: '0.75rem',
            borderTop: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.8rem',
            color: 'var(--text-muted)',
          }}
        >
          {trend && (
            <span style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>{trend}</span>
          )}
          {subtitle && <span>{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
