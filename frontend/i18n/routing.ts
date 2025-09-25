import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  // 支持的语言列表
  locales: ['en', 'zh'],
  // 默认语言
  defaultLocale: 'zh',
  // 使用路径前缀而不是URL中的语言标识符
  localePrefix: 'as-needed',
});
