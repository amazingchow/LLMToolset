'use client';

import { useTheme } from '@/lib/context/theme-context';
import { Button } from '@/components/ui/button';

export function ThemeToggleButton() {
  // 获取当前主题和切换主题状态的函数
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      className="bg-background hover:bg-accent hover:text-accent-foreground relative h-6 w-6"
      aria-label={`切换到${theme === 'light' ? '深色' : '浅色'}模式`}
    >
      {/* 太阳图标 (浅色模式时显示) */}
      <svg
        className={`h-4 w-4 transition-all duration-300 ${
          theme === 'dark' ? 'scale-0 rotate-90' : 'scale-100 rotate-0'
        }`}
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <circle cx="12" cy="12" r="5" />
        <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
      </svg>
      {/* 月亮图标 (深色模式时显示) */}
      <svg
        className={`absolute h-4 w-4 transition-all duration-300 ${
          theme === 'dark' ? 'scale-100 rotate-0' : 'scale-0 -rotate-90'
        }`}
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
      </svg>
    </Button>
  );
}
