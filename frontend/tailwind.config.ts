import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class', // 使用 class 策略来切换 dark mode
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  plugins: [],
};

export default config;
