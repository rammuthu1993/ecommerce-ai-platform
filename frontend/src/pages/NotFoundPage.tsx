import React from 'react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div style={{ maxWidth: '600px', margin: '5rem auto', textAlign: 'center', padding: '2rem' }}>
      <h1 style={{ fontSize: '4rem', fontWeight: 800, color: 'var(--accent-primary)' }}>404</h1>
      <h2 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: '1rem' }}>Page Not Found</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        The page you are looking for does not exist or has been moved.
      </p>
      <Link
        to="/"
        style={{
          padding: '0.75rem 1.5rem',
          borderRadius: 'var(--radius-md)',
          background: 'var(--accent-primary)',
          color: '#fff',
          fontWeight: 600,
        }}
      >
        Return to Home
      </Link>
    </div>
  );
};
