# franciscaineditos

Selección manual de los textos inéditos de Francisca Julián Querol (Cinctorres, 1945).

Es el segundo intento de lo que se hizo en
[franciscapublicaciones](https://github.com/jtpadilla/franciscapublicaciones). Aquel primer intento
procesó de forma automática los 6.729 ficheros recuperados de sus ordenadores y su Drive, y el
resultado fue tan masivo que se perdió el control sobre qué documentos quedaron al final.

Aquí se va despacio y a mano: los documentos entran por tandas, se leen uno a uno y cada decisión
queda anotada. Lo que venga después (publicación, site) se decidirá cuando la selección esté hecha.

## Cómo funciona una tanda

```
raw/  ──convierte.py──>  inprocess/  ──selección y regularización──>  md/<obra>/
```

1. Se dejan los originales en bruto (docx, doc, odt, txt, con sus carpetas) en `raw/`.
2. `tools/convierte.py --todo` los pasa a markdown en `inprocess/`, con sus imágenes, y `raw/` se vacía.
3. En `inprocess/` se leen, se descartan duplicados, copias, textos ajenos y restos, y se agrupan por tema.
4. Cada grupo con entidad pasa a una **obra** de `md/`, nueva o existente, regularizado: cabecera mínima,
   formato común, título y nombre coherentes con el contenido, imágenes enlazadas. Lo que pasa a `md/`
   desaparece de `inprocess/`.
5. `tools/indice.py` regenera los índices y `tools/comprueba.py` verifica las normas de `md/`.

El detalle del procedimiento, con los criterios de decisión, está en `CLAUDE.md`; el mapa de obras, las
obras pendientes y el destino de cada bloque de material, en `OBRAS.md`.

## Qué hay aquí

| | |
|---|---|
| `raw/` | bandeja de entrada. Normalmente vacía; lo que se deja dentro no entra en el repositorio. |
| `inprocess/` | los documentos de la tanda en curso, un markdown por documento con sus imágenes en `img/`. Vacío entre tandas. |
| `md/` | **los documentos seleccionados**, organizados por obra: `md/<obra>/<documento>/index.md` y su `img/`. Cada obra tiene `_carpeta.md` (id, título, criterio de qué va en ella, notas) y un `INDICE.md`. |
| `tools/convierte.py` | `raw/` a `inprocess/` con pandoc y LibreOffice. Asigna ids y no repite lo ya convertido. |
| `tools/indice.py` | regenera `inprocess/INDICE.md`, `md/INDICE.md` y el `INDICE.md` de cada obra. |
| `tools/comprueba.py` | verifica las normas de `md/`: imágenes enlazadas, cabeceras, títulos, criterios, ids únicos. |

Cada documento de `md/` empieza con una cabecera YAML de tres campos: `id` (fijo, tres cifras), `titulo` y
`notas`, donde consta de dónde sale, qué versiones había y cualquier duda de autoría.

## Las obras

| Id | Obra | Docs | Qué contiene |
|---|---|---|---|
| C12 | Memoria familiar | 11 | el libro de memorias (2026), la versión de 2014 con fotos, la tapa, la genealogía de los Julián Segura y los Boix, recuerdos sueltos |
| C19 | Familia Padilla Agut | 1 | la familia de su marido: la abuela María |
| C08 | Religion | 12 | los trabajos del curso de religión medieval de la Universitat per a Majors |
| C20 | Poemes i reflexions | 16 | poemas y textos breves de reflexión |
| C21 | Cinctorres | 13 | historia, patrimonio, oficios y fiestas del pueblo |
| C22 | Món rural i cuina | 10 | agricultura, masías, saberes del campo y recetas |
| C23 | Relats | 5 | cuentos y relatos |
| C24 | Castelló | 6 | la ciudad y su término |
| C25 | Listo | 14 | las entradas del blog narradas por el perro Listo |
| C26 | Treballs i reflexions | 10 | trabajos de curso y textos de opinión |
| C27 | Polo de Bernabé | 2 | la investigación genealógica sobre esa familia |

## Estado

- 2026-09-05, primera tanda: 449 ficheros en `raw/`. Descartados multimedia, PDF, hojas de cálculo y
  presentaciones; 183 documentos de texto convertidos a `inprocess/`; tras la selección, **100 documentos
  en 11 obras** en `md/`. `inprocess/` y `raw/` vacíos, listos para la siguiente tanda.
- Ids de documento usados hasta el 174 y de obra hasta C27; los siguientes continúan desde ahí.

## De dónde sale el fondo

`../franciscapublicaciones/` (el primer intento, con su corpus) y `../franciscabacket/` (el resto del fondo,
5,5 GB, con 36 PDF escaneados y 2 OneNote pendientes de OCR). Son solo lectura: no se modifican, no se borran
y no se usan para buscar candidatos; los documentos entran únicamente por `raw/`.
