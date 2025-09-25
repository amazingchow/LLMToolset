'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';

// 支持的主题类型
type Theme = 'light' | 'dark';
// Context 对象类型
interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}
// 创建 Context 对象
const ThemeContext = createContext<ThemeContextType>({
  theme: 'light' as Theme,
  toggleTheme: () => {},
});
// Provider 组件类型
interface ThemeProviderProps {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
}
// 创建 Provider 组件
export function ThemeProvider({ children, defaultTheme = 'light', storageKey = 'theme' }: ThemeProviderProps) {
  const [mounted, setMounted] = useState(false);
  const [theme, setThemeState] = useState<Theme>(() => {
    // 只有在客户端才尝试读取 localStorage
    if (typeof window !== 'undefined') {
      try {
        const savedTheme = localStorage.getItem(storageKey) as Theme;
        if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
          return savedTheme;
        }
        // 如果没有保存的主题，检查系统偏好
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        return systemTheme;
      } catch (error) {
        console.warn('Failed to read theme from localStorage:', error);
      }
    }
    // 在 SSR 期间使用默认主题，避免水合不匹配
    return defaultTheme;
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const root = window.document.documentElement;
    // 移除之前的主题类
    root.classList.remove('light', 'dark');
    // 添加当前主题类
    root.classList.add(theme);

    // 保存到 localStorage
    try {
      localStorage.setItem(storageKey, theme);
    } catch (error) {
      console.warn('Failed to save theme to localStorage:', error);
    }
  }, [theme, storageKey, mounted]);

  // 防止水合不匹配，在客户端挂载前不渲染
  if (!mounted) {
    return <div style={{ visibility: 'hidden' }}>{children}</div>;
  }

  const toggleTheme = () => {
    setThemeState((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const value: ThemeContextType = {
    theme,
    toggleTheme,
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  return context;
}
