'use client';

import Link from 'next/link';
import { GalleryVerticalEnd } from 'lucide-react';
import { useTranslations } from 'next-intl';

import { LocaleToggleButton } from '@/components/locale-toggle-button';
import { ThemeToggleButton } from '@/components/theme-toggle-button';

interface HeaderProps {
  showControls?: boolean;
}

export function Header({ showControls = true }: HeaderProps) {
  const t = useTranslations('Common');

  return (
    <header className="border-border bg-card border-b">
      <div className="container mx-auto flex items-center justify-between px-2 py-2">
        <Link href="/" className="flex items-center gap-4">
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <GalleryVerticalEnd className="size-4" />
          </div>
          {t('brand')}
        </Link>
        {showControls && (
          <div className="flex items-center gap-4">
            <LocaleToggleButton />
            <ThemeToggleButton />
          </div>
        )}
      </div>
    </header>
  );
}
