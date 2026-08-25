import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: string) => boolean;
  isAdmin: boolean;
  isManager: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('user_profile');
    try {
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    if (token) {
      authService
        .getProfile()
        .then((res) => {
          if (res.data) {
            setUser(res.data);
            localStorage.setItem('user_profile', JSON.stringify(res.data));
          }
        })
        .catch((err) => {
          // If no stored profile exists, clear session
          if (!localStorage.getItem('user_profile')) {
            logout();
          }
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await authService.login({ email, password });
    const newToken = res.data.access_token;
    const userData = res.data.user;
    console.log(userData, "user")
    localStorage.setItem('access_token', newToken);
    localStorage.setItem('user_profile', JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
  };

  const register = async (username: string, email: string, password: string) => {
    const res = await authService.register({ username, email, password });
    const newToken = res.data.access_token;
    const userData = res.data.user;
    setUser(userData)
    localStorage.setItem('access_token', newToken);
    localStorage.setItem('user_profile', JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_profile');
    setToken(null);
    setUser(null);
  };

  const hasRole = (role: string) => {
    if (!user) return false;
    const targetRole = role.toUpperCase();
    const rawRoles = user.roles || (user as any).role || (user as any).user_roles || [];
    const rolesArray = Array.isArray(rawRoles) ? rawRoles : [rawRoles];

    return rolesArray.some((r: any) => {
      if (!r) return false;
      const roleStr = (typeof r === 'object' ? (r.name || r.role || JSON.stringify(r)) : String(r)).toUpperCase();
      return roleStr.includes(targetRole) || targetRole.includes(roleStr);
    });
  };

  const isAdmin =
    hasRole('ADMIN') ||
    (user as any)?.is_admin === true ||
    (user?.email ? user.email.toLowerCase().includes('admin') : false);

  const isManager =
    hasRole('MANAGER') ||
    isAdmin ||
    (user as any)?.is_manager === true ||
    (user?.email ? user.email.toLowerCase().includes('manager') : false) ||
    (user !== null && user.id === 1);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login,
        register,
        logout,
        hasRole,
        isAdmin,
        isManager,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
