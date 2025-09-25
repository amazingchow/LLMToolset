'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { usePathname, useRouter } from '@/i18n/navigation';
import { routing } from '@/i18n/routing';

// 支持的语言类型
type Locale = 'en' | 'zh';
// Context 对象类型
interface LocaleContextType {
  locale: Locale;
  toggleLocale: () => void;
}
// 创建 Context 对象
const LocaleContext = createContext<LocaleContextType>({
  locale: 'zh' as Locale,
  toggleLocale: () => {},
});
// Provider 组件类型
interface LocaleProviderProps {
  children: React.ReactNode;
  defaultLocale?: Locale;
  storageKey?: string;
}
// 创建 Provider 组件
export function LocaleProvider({ children, defaultLocale = 'zh', storageKey = 'locale' }: LocaleProviderProps) {
  const [mounted, setMounted] = useState(false);
  const [locale, setLocaleState] = useState<Locale>(() => {
    // 只有在客户端才尝试读取 localStorage
    if (typeof window !== 'undefined') {
      try {
        const savedLocale = localStorage.getItem(storageKey) as Locale;
        if (savedLocale && routing.locales.includes(savedLocale)) {
          return savedLocale;
        }
        // 如果没有保存的主题，检查系统偏好
        const systemLocale = window.navigator.language.split('-')[0];
        if (routing.locales.includes(systemLocale as Locale)) {
          return systemLocale as Locale;
        }
        return defaultLocale;
      } catch (error) {
        console.warn('Failed to read locale from localStorage:', error);
      }
    }
    // 在 SSR 期间使用默认语言, 避免水合不匹配
    return defaultLocale;
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!mounted) return;

    // 保存到 localStorage
    try {
      localStorage.setItem(storageKey, locale);
    } catch (error) {
      console.warn('Failed to save locale to localStorage:', error);
    }

    // 使用 next-intl 的导航进行路由切换
    router.push(pathname, { locale: locale });
  }, [locale, storageKey, mounted, router, pathname]);

  // 防止水合不匹配，在客户端挂载前不渲染
  if (!mounted) {
    return <div style={{ visibility: 'hidden' }}>{children}</div>;
  }

  const toggleLocale = () => {
    setLocaleState((prev) => (prev === 'en' ? 'zh' : 'en'));
  };

  const value: LocaleContextType = {
    locale,
    toggleLocale,
  };

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const context = useContext(LocaleContext);
  return context;
}
