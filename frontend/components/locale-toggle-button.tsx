'use client';

import { useLocale } from '@/lib/context/locale-context';
import { Button } from '@/components/ui/button';

export function LocaleToggleButton() {
  // 获取当前语言和切换语言状态的函数
  const { locale, toggleLocale } = useLocale();

  const getLocaleDisplayName = (locale: string) => {
    switch (locale) {
      case 'en':
        return 'En';
      case 'zh':
        return 'Zh';
      default:
        return locale;
    }
  };

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleLocale}
      className="bg-background hover:bg-accent hover:text-accent-foreground relative h-6 w-6"
      aria-label={`切换到${locale === 'en' ? '中文' : '英文'}模式`}
    >
      <span style={{ fontSize: '0.6rem' }}>{getLocaleDisplayName(locale)}</span>
    </Button>
  );
}
