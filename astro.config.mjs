// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://wangzhi.github.io',
  vite: {
    plugins: [tailwindcss()],
  },
});
