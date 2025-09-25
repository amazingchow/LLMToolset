import type { NextConfig } from 'next';
import createNextIntlPlugin from 'next-intl/plugin';

const nextConfig: NextConfig = {
  // 重写 Google Fonts 请求到国内镜像
  async rewrites() {
    return [
      {
        source: '/fonts.googleapis.com/:path*',
        destination: 'https://fonts.font.im/:path*',
      },
      {
        source: '/fonts.gstatic.com/:path*',
        destination: 'https://gstatic.font.im/:path*',
      },
    ];
  },
};
const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
