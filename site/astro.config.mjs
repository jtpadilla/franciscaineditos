// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Mateixa família que els altres llocs de l'autora: Astro, GitHub Pages, fonts servides des del propi lloc.
// El valencià va a l'arrel i el castellà sota /es/. El repositori es diu franciscaineditos i el lloc penja d'eixa subruta.
export default defineConfig({
  site: 'https://jtpadilla.github.io',
  base: '/franciscaineditos',
  trailingSlash: 'always',
  i18n: { defaultLocale: 'ca', locales: ['ca', 'es'], routing: { prefixDefaultLocale: false } },
  integrations: [sitemap({ i18n: { defaultLocale: 'ca', locales: { ca: 'ca-ES', es: 'es-ES' } } })],
  fonts: [
    { provider: fontProviders.fontsource(), name: 'Literata', cssVariable: '--f-lectura',
      weights: [400, 600, 700], styles: ['normal', 'italic'], subsets: ['latin', 'latin-ext'],
      fallbacks: ['Georgia', 'Times New Roman', 'serif'] },
    { provider: fontProviders.fontsource(), name: 'Source Sans 3', cssVariable: '--f-ui',
      weights: [400, 600], styles: ['normal'], subsets: ['latin', 'latin-ext'],
      fallbacks: ['Helvetica Neue', 'Arial', 'sans-serif'] },
  ],
  // md/ viu a l'arrel del repositori, fora de site/
  vite: { server: { fs: { allow: ['..'] } } },
  image: { layout: 'constrained', responsiveStyles: true, breakpoints: [480, 900, 1400] },
});
