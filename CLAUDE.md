# franciscaineditos — guía de trabajo

## Qué es

Selección manual de los textos inéditos de Francisca Julián Querol (Cinctorres, 1945). Segundo
intento de `../franciscapublicaciones`. El primero fue un pipeline automático de seis fases sobre
6.729 ficheros y el usuario perdió el control sobre los documentos resultantes. Este va lento y
manual: de momento solo se seleccionan documentos, uno a uno, según instrucciones del usuario.

## Normas de md/ (dictadas por el usuario el 2026-09-05)

El objetivo es migrar una cantidad enorme de documentos que en origen están ordenados de forma caótica.

- `md/` es la lista de **obras**: una carpeta por obra, con su `_carpeta.md` (id, titulo, criterio, notas).
  Dentro de cada obra, una carpeta por **documento** con `index.md` y, opcionalmente, `img/`. Nada más:
  ni subcarpetas ni ficheros sueltos.
- **Identificador canónico** de un documento: su ruta, `md/<obra>/<documento>`. Además lleva su `id` numérico.
- **Todas las imágenes de `img/` están enlazadas** desde el `index.md`, y todo enlace existe. Si no, es un error.
- **Los documentos de una obra comparten estilo** (ver "Formato de los documentos en md/") y tienen título y
  nombre de carpeta coherentes entre sí y **coherentes con el contenido**, no con el nombre del fichero original.
- El `INDICE.md` de cada obra empieza con el **criterio**: qué tipo de documentos van en esa obra. Sirve para
  buscar candidatos en `inprocess/`. Se escribe en el campo `criterio` de `_carpeta.md`.
- Cuando un documento pasa de `inprocess/` a `md/`, lo mueva el usuario o el LLM, hay que **regularizarlo**
  (cabecera mínima, formato, nombre, título) y **retirarlo de `inprocess/`**. No puede estar en los dos sitios.
- `raw/` es donde el usuario deposita ficheros y directorios en bruto; el LLM los convierte a markdown en
  `inprocess/` con `tools/convierte.py --todo` y vacía `raw/`.
- `python3 tools/comprueba.py` verifica todo esto sobre `md/` y sale con error si algo falla. Ejecutarlo
  después de cualquier cambio en `md/`, junto con `python3 tools/indice.py`.

## Procedimiento: pasar una carpeta (Cnn) de inprocess/ a md/

Es lo que se hizo con C08 (Religión) y C12 (Memoria familiar). Repetirlo igual cuando el usuario diga
"pásame la estructura Cnn a md e intenta mejorar los documentos".

1. **Mover la carpeta entera** con `mv` a `md/<Nombre>` (index.md e img/ juntos; ver aviso más abajo).
   Conserva su `_carpeta.md` y por tanto su id. Regenerar índices: `python3 tools/indice.py`.
2. **Leer todos los documentos**, principio y final: en los finales están las firmas y fechas. Identificar
   (a) textos ajenos: firmados por otra persona, cabeceras "per Nombre - fecha" del aula virtual, "Fuente: ...";
   (b) duplicados y versiones: comparar por párrafos comunes (set de párrafos normalizados) y por
   `difflib.SequenceMatcher`; mirar qué párrafos tiene cada versión que la otra no; (c) pares del mismo texto
   en dos lenguas; (d) restos de web: iconos, píxeles 1x1, tablas HTML.
3. **Decidir con el usuario**: anotar los hallazgos en `notas` y NO borrar nada por cuenta propia. Cuando él lo
   diga: de los duplicados queda la versión más completa o más reciente; de los pares, la de catalán/valencià;
   los ajenos se borran. Si un documento ajeno lleva dentro un texto suyo (una felicitación, un capítulo),
   ese texto se salva como documento propio con el id del original y una nota que diga de dónde sale.
4. **Cabecera mínima** en md/: solo `id`, `titulo`, `notas`. Quitar origen, formato, caracteres, imagenes, interesa.
5. **Formato** (ver "Formato de los documentos en md/"). Se hace con un script de un solo uso sobre la carpeta,
   nunca a mano documento a documento, y después se revisa la estructura de cada uno con
   `grep -n '^#\|^\*[^*].*\*$'` y se corrigen a mano los falsos títulos (listas, vocabularios) y los
   títulos que faltan. Puntos que fallaron y hay que vigilar: los espacios dentro de `**`, que hay que tratar
   por bloques `**texto**` y no con regex de un solo lado; los `<u>` que al pasar a negrita se convierten en
   título por error; las líneas largas convertidas en `#` por pandoc, que son párrafos; el título repetido
   justo debajo del H1.
6. **Nombres de carpeta y `titulo`**: mayúscula solo al inicio y en nombres propios, con acentos, sin números
   ni puntos de los nombres de fichero, en la lengua del texto. El H1 del cuerpo es igual al `titulo`.
   Los títulos que ella escribió dentro del texto (en mayúsculas o como sea) no se tocan.
7. **Comprobar** que ninguna referencia `![](img/...)` apunta a un fichero inexistente, regenerar índices y
   dar al usuario un resumen con lo que se ha borrado, lo que se ha conservado y por qué, y lo que queda a
   su decisión.

## Formato de los documentos en md/

Título de nivel uno igual al `titulo` de la cabecera. Secciones en nivel dos. Subrayados convertidos a negrita.
Imágenes en párrafo propio, con el pie en cursiva debajo. Firmas y fechas finales en cursiva. Sin líneas
vacías de relleno ni negritas rotas. El texto de la autora no se toca; solo el formato. Los textos firmados
por otras personas se anotan en `notas` y se dejan a la decisión del usuario.

## Cómo trabajar aquí

- **Esperar instrucciones.** El usuario irá diciendo qué ficheros incorporar y qué hacer con cada uno.
  No montar pipelines, scripts de proceso masivo ni estructura de site por adelantado.
- **No automatizar sin que lo pida.** Si una tarea repetitiva se puede resolver con un script pequeño,
  proponerlo antes, no ejecutarlo.
- **Leer antes de decidir.** Lección del primer intento: el formato no dice la autoría, el nombre del
  fichero no dice el contenido y ningún score automático separa bien lo suyo de lo ajeno.
- **Los textos de la autora no se corrigen ni se retocan.** Van en la lengua en que ella los escribió
  (valencià o castellano).
- **Anotar cada decisión** de inclusión o exclusión con su motivo, en el sitio que se acuerde con el
  usuario cuando haya documentos.
- **Al reorganizar md/, mover carpetas enteras** (index.md + img/), nunca escribir solo un index.md nuevo y borrar
  la carpeta vieja: así se perdieron las imágenes de Memòria familiar el 2026-09-05 (recuperadas del corpus de
  ../franciscapublicaciones). raw/ se vacía tras convertir, así que las imágenes de inprocess/ y md/ son la única copia local.
- Idioma de trabajo con el usuario: castellano.

## Fuentes (solo lectura, no borrar)

- `../franciscapublicaciones/corpus/<obra>/<slug>/index.md` con frontmatter YAML, `img/` y `variants/`.
- `../franciscapublicaciones/obras/obras.tsv`: 538 documentos clasificados en 25 grupos con evidencia.
- `../franciscabacket/`: todo lo demás del fondo, con README propio. Contiene los 36 PDF escaneados
  y 2 OneNote aún sin OCR.

## Estructura

```
raw/                 BANDEJA DE ENTRADA. El usuario deja aquí originales (docx, doc, odt, txt); se convierten a
                     inprocess/ con tools/convierte.py y luego raw/ se vacía. Normalmente está vacío. Los originales
                     de lo ya convertido no se conservan: el markdown de inprocess/ es la única copia.
inprocess/<ruta>/<nombre>/  un documento por carpeta, misma jerarquía que raw/. index.md + img/. Si dos
                     ficheros del mismo directorio compartían nombre, la carpeta lleva la extensión:
                     "El camí (txt)". Aquí el usuario filtra y mejora.
md/<obra>/<doc>/     LOS SELECCIONADOS, organizados por obra. Ver "Normas de md/". Nada se pone en md/ sin que
                     el usuario lo decida.
<carpeta>/_carpeta.md  en cada carpeta que agrupa documentos (no en las de documento ni en img/): cabecera con
                     id "C01", "C02"..., titulo y notas. Lo crea tools/indice.py si falta. Sirve para que el usuario
                     pueda referirse a una carpeta entera por su id.
*/INDICE.md          tabla generada en inprocess/ y en md/, en orden de árbol, con las carpetas en negrita y sus
                     documentos debajo. Además, en md/ cada carpeta tiene su propio INDICE.md con lo que cuelga
                     de ella y un enlace al índice superior. No editarlos a mano: editar cabeceras y regenerar.
tools/convierte.py   raw/ -> inprocess/. Sin rutas no hace nada; --todo lo recorre entero. Salta las carpetas que ya existen (para no pisar ediciones del
                     usuario); --forzar las regenera. Acepta rutas dentro de raw/ para convertir una parte.
                     Asigna a los documentos nuevos el siguiente id libre; con --forzar conserva el que tenían.
                     Reconoce cada documento por el campo origen de la cabecera, no por el nombre de carpeta:
                     lo que ya está en inprocess/ o en md/ se salta aunque se haya renombrado. Lo de md/ no se
                     regenera ni con --forzar.
tools/indice.py      regenera inprocess/INDICE.md, md/INDICE.md y el INDICE.md de cada obra; crea los _carpeta.md que falten.
tools/comprueba.py   comprueba las normas de md/ (imágenes enlazadas, cabeceras, H1 = titulo, criterio, ids únicos).
```

Pandoc está en `~/.local/bin/pandoc` (3.6.4, binario descargado; no viene de apt). LibreOffice 7.3 en
`/usr/bin/soffice`. Los doc y odt pasan por LibreOffice a docx en un temporal y luego por pandoc.

## Cabecera de cada index.md

En md/ la cabecera es mínima: solo `id`, `titulo` y `notas`. Estar en md/ ya significa "seleccionado", así
que no se guarda origen, formato, tamaño ni `interesa`. En inprocess/ se conserva la cabecera completa:

```yaml
id: "011"                    # fijo para siempre, tres cifras. Es como el usuario se refiere a un documento.
titulo: "La cadira"          # editable por el usuario
origen: "CEVA/La cadira.docx" # ruta en raw/, la única clave que une md con el original. No cambiar.
formato: "docx"
caracteres: 1259              # sin contar las referencias a imágenes
imagenes: 0
interesa: ""                  # el usuario pone: sí / no / duda
notas: ""                     # el usuario escribe lo que quiera
```

El usuario revisa en el IDE con la previsualización de markdown. Puede renombrar carpetas: `origen`
en la cabecera sigue diciendo de dónde venía. Como raw/ se vacía tras convertir, no hay forma de
regenerar un documento desde el original: las ediciones del usuario sobre el markdown son definitivas.

Tras cualquier cambio en cabeceras o movimiento entre inprocess/ y md/, ejecutar `python3 tools/indice.py`.
