import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { slug } from './site/slug';

// El master és md/, a l'arrel del repositori: una carpeta per obra amb _carpeta.md (id, titulo, criterio, notas)
// i dins una carpeta per document amb index.md (id, titulo, notas) i img/. El lloc només el llig.
// Els identificadors es fan a partir del nom de carpeta, sense accents ni majúscules, per a les URL.
const generateId = ({ entry }: { entry: string }) =>
  entry.replace(/\/?(index|_carpeta)\.md$/, '').split('/').map(slug).join('/');

export const collections = {
  textos: defineCollection({
    loader: glob({ pattern: '*/*/index.md', base: '../md', generateId }),
    schema: z.object({ id: z.string(), titulo: z.string(), notas: z.string() }),
  }),
  obres: defineCollection({
    loader: glob({ pattern: '*/_carpeta.md', base: '../md', generateId }),
    schema: z.object({ id: z.string(), titulo: z.string(), criterio: z.string(), notas: z.string() }),
  }),
};
