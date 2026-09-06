/** Nom de carpeta -> tros d'URL: sense accents, minúscules, guions. «Món rural i cuina» -> «mon-rural-i-cuina». */
export const slug = (s: string) =>
  s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[’'`]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
