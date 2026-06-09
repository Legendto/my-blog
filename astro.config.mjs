// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 站点配置
const SITE_URL = process.env.SITE_URL || 'https://example.vercel.app';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'never',
  build: {
    format: 'directory'
  },
  integrations: [
    sitemap()
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
      wrap: true
    }
  },
  vite: {
    build: {
      cssCodeSplit: true
    }
  }
});