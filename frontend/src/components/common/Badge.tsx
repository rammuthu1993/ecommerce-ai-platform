import React from 'react';

interface BadgeProps {
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'primary' | 'secondary';
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ variant = 'primary', children, className = '' }) => {
  const styles: Record<string, string> = {
    success: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    warning: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    danger: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
    info: 'bg-sky-500/20 text-sky-400 border-sky-500/30',
    primary: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
    secondary: 'bg-slate-700/50 text-slate-300 border-slate-600/30',
  };

  const styleClass = styles[variant] || styles.primary;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '0.25rem 0.65rem',
        borderRadius: '9999px',
        fontSize: '0.75rem',
        fontWeight: 600,
        border: '1px solid',
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
      }}
      className={`${styleClass} ${className}`}
    >
      {children}
    </span>
  );
};
