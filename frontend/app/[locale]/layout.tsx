// app/layout.tsx is the root layout for the app
import type { Metadata } from 'next';
import { Inter, JetBrains_Mono, Noto_Sans_SC } from 'next/font/google';
import { NextIntlClientProvider } from 'next-intl';

import { LocaleProvider } from '@/lib/context/locale-context';
import { QueryClientProviderWrapper } from '@/lib/context/query-client-context';
import { ThemeProvider } from '@/lib/context/theme-context';
import { Header } from '@/components/header';

import '@/app/[locale]/styles/globals.css';

// 主字体 - Inter 支持中英文混排
const inter = Inter({
  variable: '--font-inter',
  subsets: ['latin'],
  display: 'swap',
});

// 等宽字体 - JetBrains Mono 适合代码显示
const jetbrainsMono = JetBrains_Mono({
  variable: '--font-jetbrains-mono',
  subsets: ['latin'],
  display: 'swap',
});

// 中文字体 - Noto Sans SC 专为简体中文优化
const notoSansSC = Noto_Sans_SC({
  variable: '--font-noto-sans-sc',
  subsets: ['latin'],
  weight: ['300', '400', '500', '700'],
  display: 'swap',
});

// 支持的语言
const locales = ['en', 'zh'];

export const metadata: Metadata = {
  title: 'LLMToolset',
  description: '面向大型语言模型 (LLMs) 开发与运维的实用工具集合',
};

type Props = {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
};

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;
  // 验证 locale 是否有效，如果无效则使用默认语言
  const validLocale = locales.includes(locale) ? locale : 'en';
  return (
    <html lang={validLocale} suppressHydrationWarning>
      <body className={`${inter.variable} ${jetbrainsMono.variable} ${notoSansSC.variable}`}>
        <NextIntlClientProvider locale={validLocale}>
          <LocaleProvider defaultLocale={validLocale as 'en' | 'zh'}>
            <ThemeProvider>
              <div className="bg-background text-foreground min-h-screen">
                <Header />
                <QueryClientProviderWrapper>
                  <main>{children}</main>
                </QueryClientProviderWrapper>
              </div>
            </ThemeProvider>
          </LocaleProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
