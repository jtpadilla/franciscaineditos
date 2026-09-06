import { getCollection } from 'astro:content';
import { OBRES } from '../site/config';

/** Totes les rutes del lloc (sense idioma): portada, obres, textos, fotografies, cerca, sobre. */
export async function rutes() {
  const textos = await getCollection('textos');
  const out: { params: { ruta: string | undefined }; props: { tipus: string; obra?: string; id?: string } }[] = [
    { params: { ruta: undefined }, props: { tipus: 'portada' } },
    { params: { ruta: 'fotografies' }, props: { tipus: 'fotografies' } },
    { params: { ruta: 'cerca' }, props: { tipus: 'cerca' } },
    { params: { ruta: 'sobre' }, props: { tipus: 'sobre' } },
    { params: { ruta: 'autora' }, props: { tipus: 'autora' } },
  ];
  const obres = new Set([...Object.keys(OBRES), ...textos.map((t) => t.id.split('/')[0])]);
  for (const o of obres) out.push({ params: { ruta: `obres/${o}` }, props: { tipus: 'obra', obra: o } });
  for (const t of textos) out.push({ params: { ruta: `obres/${t.id}` }, props: { tipus: 'text', id: t.id } });
  return out;
}
