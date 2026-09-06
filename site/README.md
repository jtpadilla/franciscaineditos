# Escrits inèdits

Els textos de Francisca Julián Querol que no havien eixit mai de l’ordinador, triats un a un: les memòries,
el treball sobre l’agricultura i els costums del món rural, Cinctorres i Castelló, les entrades de Listo,
els treballs de curs, els poemes, la biodiversitat de la Rambla Celumbres. 144 textos en 12 obres, en
valencià (arrel) i castellà (`/es/`), publicats a <https://jtpadilla.github.io/franciscaineditos/>.

Lloc Astro 7, publicat a GitHub Pages amb cada push a `main` (`.github/workflows/deploy.yml`, a l’arrel del
repositori). Forma part de la família de llocs de l’autora i seguix les seues convencions: la mateixa base
que «Escrits inèdits» de franciscapublicaciones i el buscador amb filtres de «Les meues coses».

## D’on ve el contingut

De `../md/<obra>/<document>/index.md`, a l’arrel del repositori: **md/ és el master i este lloc només el llig**
(`src/content.config.ts`, `base: '../md'`). Cada obra té el seu `_carpeta.md` (id, títol, criteri, notes) i cada
document una capçalera mínima (id, títol, notes) i les seues imatges a `img/`. No hi ha cap pas de generació ni
còpia intermèdia. Els identificadors de les URL ixen del nom de carpeta sense accents (`src/site/slug.ts`).
La llengua de cada text, la longitud i el nombre d’imatges es calculen en construir (`src/site/llengua.ts`).
Abans de construir, el workflow executa `python3 tools/comprueba.py`.

## Estructura

| | |
|---|---|
| `astro.config.mjs` | `base: /franciscaineditos`, fonts Literata i Source Sans 3 servides des del propi lloc, imatges `constrained` |
| `src/site/config.ts` | noms i descripcions de les obres en les dues llengües, cadenes de la interfície, llocs germans |
| `src/vistas/Pagina.astro` | totes les vistes: portada, obra, text, fotografies, cerca, sobre |
| `src/vistas/rutes.ts` | les rutes, compartides pels dos idiomes |
| `src/pages/[...ruta].astro`, `src/pages/es/[...ruta].astro` | la mateixa vista en `ca` i `es` |
| `src/layouts/Base.astro` | capçalera, tema clar o fosc, visor d’imatges, peu |

La cerca és [Pagefind](https://pagefind.app/): l’índex es genera després de construir (`npm run build`) i es
consulta al navegador, sense servidor; els filtres són l’obra i la llengua, i cada idioma del lloc busca en
les seues pàgines.

```
npm install && npm run build   # dist/, 321 pàgines + índex de cerca, ~185 MB
npx astro preview              # http://127.0.0.1:4321/franciscaineditos/
```
