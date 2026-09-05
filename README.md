# franciscaineditos

Selección manual de los textos inéditos de Francisca Julián Querol (Cinctorres, 1945).

Es el segundo intento de lo que se hizo en
[franciscapublicaciones](https://github.com/jtpadilla/franciscapublicaciones). Aquel primer intento
procesó de forma automática los 6.729 ficheros recuperados de sus ordenadores y su Drive, y el
resultado fue tan masivo que se perdió el control sobre qué documentos quedaron al final.

Aquí se va despacio y a mano: los documentos se incorporan uno a uno, leyéndolos, y cada decisión
queda anotada. De momento el proyecto consiste únicamente en hacer esa selección. Lo que venga
después (publicación, site) se decidirá cuando la selección esté hecha.

## De dónde salen los documentos

- `../franciscapublicaciones/corpus/`: el corpus del primer intento, 164 textos en 15 obras.
- `../franciscapublicaciones/obras/obras.tsv`: la clasificación de los 538 documentos del fondo.
- `../franciscabacket/`: el resto del fondo (5,5 GB), incluidos 36 PDF escaneados y 2 OneNote
  pendientes de OCR.

Ninguna de esas fuentes se modifica ni se borra.

## Qué hay aquí

| | |
|---|---|
| `raw/` | bandeja de entrada: aquí se dejan los originales (docx, doc, odt, txt) para convertirlos. Se vacía después. |
| `inprocess/` | un markdown por documento, en `inprocess/<misma ruta>/<nombre>/index.md`, con sus imágenes en `img/`. Aquí se filtran y se mejoran. |
| `md/` | los documentos seleccionados, organizados por obra: `md/<obra>/<documento>/index.md` con su `img/`. Cada obra tiene `_carpeta.md` con el criterio de qué va en ella y un `INDICE.md`. |
| `INDICE.md` | en `inprocess/` y en `md/`: tabla en orden de árbol con carpetas y documentos, sus ids, estado y notas. Se regenera con `tools/indice.py`. |
| `_carpeta.md` | en cada carpeta que agrupa documentos: su id (`C01`, `C02`...), título y notas. |
| `tools/convierte.py` | convierte `raw/` a `inprocess/` (pandoc, y LibreOffice para doc y odt). No pisa lo ya convertido salvo con `--forzar`. |
| `tools/indice.py` | regenera los `INDICE.md` (general de `inprocess/` y de `md/`, y uno por obra) a partir de las cabeceras. |
| `tools/comprueba.py` | comprueba las normas de `md/`: imágenes enlazadas, cabeceras, títulos, criterios, ids únicos. |

Cada `index.md` empieza con una cabecera YAML: `id` (fijo, tres cifras), `titulo`, `origen` (ruta en `raw/`), `formato`,
`caracteres`, `imagenes`, `interesa` y `notas`. La revisión consiste en ir leyendo cada documento
y rellenar `interesa` (sí, no, duda) y `notas`, cambiar el título si hace falta y, si conviene,
retocar el formato del markdown. Cuando un documento está listo, su carpeta se mueve de `inprocess/`
a `md/`.

## Estado

2026-09-05: `raw/` limpio de multimedia, PDF, hojas de cálculo y presentaciones. Los documentos
de texto convertidos a markdown en `inprocess/`. Selección en marcha en `inprocess/`; `raw/` vaciado, a la
espera de la siguiente tanda de originales. `md/` vacío todavía.
# franciscaineditos
