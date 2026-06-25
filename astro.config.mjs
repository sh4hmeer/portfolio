// @ts-check
import { defineConfig } from 'astro/config';

// Deploy target: GitHub Pages on the `sh4hmeer` account, served at the apex
// custom domain shahmeershahid.com (public/CNAME). base stays '/' for an apex
// domain. Repo: github.com/sh4hmeer/portfolio, built by .github/workflows/deploy.yml.
export default defineConfig({
  site: 'https://shahmeershahid.com',
  base: '/',
  build: { assets: '_astro' },
});
