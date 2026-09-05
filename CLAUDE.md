# franciscaineditos — guía de trabajo

## Qué es

Selección manual de los textos inéditos de Francisca Julián Querol (Cinctorres, 1945). Segundo intento
de `../franciscapublicaciones`. El primero fue un pipeline automático de seis fases sobre 6.729 ficheros y
el usuario perdió el control sobre los documentos resultantes. Este va lento y manual, por tandas.

Idioma de trabajo con el usuario: castellano. Los textos de la autora van en la lengua en que ella los
escribió (valencià o castellano) y **no se corrigen ni se retocan**; solo se les da formato.

## Estado (2026-09-05, fin de la primera tanda)

`md/` tiene 100 documentos en 11 obras (C08, C12, C19 a C27). `inprocess/` y `raw/` están vacíos.
Último id de documento usado: 174. Última obra: C27. **Se va a repetir el ciclo completo desde `raw/`
con ficheros nuevos**: seguir el procedimiento de abajo tal cual.

## El ciclo completo de una tanda

### 1. Entrada: raw/ → inprocess/

- El usuario deja en `raw/` ficheros y carpetas en bruto. Primero se hace inventario (por extensión y por
  tipo real con `file`; zip: mirar dentro) y se le presenta la lista antes de borrar. Lo que él ha mandado
  borrar en las dos primeras tandas: imágenes (jpg, png, gif, tif, jfif, psd, svg), audio y vídeo (wma, mp4,
  flv), zips de fotos, PDF, presentaciones (ppt, pptx, ppsx, pps, pptm), hojas de cálculo (xls, xlsx, ods),
  DWG, OneNote (.one, .onetoc2: no se pueden convertir), páginas web guardadas (html + carpetas `_files` con
  xml, js, php, css...), restos de sistema (.lnk, .rdp, .ini, .dropbox*, Picasa.ini, ZbThumbnail.info,
  AUTORUN.INF, desktop.ini, System Volume Information, ficheros de bloqueo `~$*.docx`), ficheros vacíos
  y carpetas vacías. Se quedan docx, doc, odt, rtf y txt.
- `python3 tools/convierte.py --todo` convierte docx, doc, odt, rtf y txt a `inprocess/<misma ruta>/<nombre>/index.md`
  con `img/`. Reconoce por el campo `origen` lo que ya existe en `inprocess/` o `md/` y no lo repite; asigna
  a cada documento nuevo el siguiente id libre. Luego `python3 tools/indice.py` (crea los `_carpeta.md`
  de las carpetas nuevas con el siguiente id Cnn).
- Comprobar que cada imagen extraída queda enlazada y que no hay imágenes pegadas al texto (el script
  ya corrige las dos cosas). Listar los documentos casi vacíos (`caracteres` < 100).
- **Comparar cada documento nuevo con los de `md/`** (`difflib` sobre el texto normalizado, prefiltro por
  longitud) y anotar en `notas` de inprocess/ "IGUAL (0.99) a md/<obra>/<doc>, ya publicado" (≥0.95),
  "CASI IGUAL" (≥0.85) o "PARECIDO" (≥0.6). Así el usuario ve en el INDICE.md qué es repetido. En la
  segunda tanda, 87 de 580 eran iguales a algo ya publicado y 41 parecidos.
- Vaciar `raw/`: el markdown de `inprocess/` pasa a ser la única copia local. `raw/` está en `.gitignore`.
- Commit: "Tanda N: conversión de raw/ a inprocess/".

### 2. Selección en inprocess/

- El usuario borra a mano lo que no quiere y va pidiendo cosas. Cuando pide **"propón la siguiente
  publicación"**: listar `inprocess/` (id, tamaño, ruta, primera línea), agrupar por tema, y proponer el
  grupo más maduro con la lista de ids, las alternativas y lo que queda fuera. Primero las obras claramente
  suyas y limpias; el material pesado o de autoría dudosa, al final.
- Cuando pide **"hay candidatos para md/<obra>?"**: buscar en `inprocess/` con el `criterio` de la obra
  (palabras clave, grep sobre el cuerpo), leer los que puntúen y decir cuáles encajan, cuáles son dudosos
  y cuáles no, con motivo. No mover nada hasta que lo diga.
- Cuando pide **"crea la publicación X y pásale los documentos"** o **"pásame la estructura Cnn a md"**,
  seguir el procedimiento de la sección siguiente.
- Al final de la tanda, **"revisa lo que queda"**: listar los restos, decir qué es cada uno (ajeno, copia de
  lo ya publicado, borrador superado, nota o prueba) y proponer destino o borrado. El usuario decide; en la
  primera tanda hizo la limpieza final a mano.

### 3. Pasar documentos a una obra de md/ (procedimiento)

1. **Leer todos los candidatos enteros**, principio y final: en los finales están las firmas y fechas.
   Identificar (a) textos ajenos: firmados por otra persona, cabeceras "per Nombre - fecha" del aula virtual,
   "Fuente: ...", letras de canciones, sonetos de Cervantes, copias de Wikipedia, MyHeritage, Geni, Geneanet;
   (b) duplicados y versiones: comparar con `difflib.SequenceMatcher` sobre el texto normalizado y por
   párrafos comunes; mirar qué tiene cada versión que la otra no; (c) pares del mismo texto en dos lenguas;
   (d) compilaciones: un fichero que reúne varias piezas (el blog de Listo entero, dos poemas en un fichero)
   se separa en un documento por pieza; (e) restos de web: iconos, píxeles 1x1, tablas HTML, `<span class="mark">`.
2. **Criterios de decisión** (los ha dado el usuario): de los duplicados queda la versión más completa o más
   reciente; de los pares en dos lenguas, la de valencià; los ajenos se borran, pero si un ajeno lleva dentro
   un texto suyo (una felicitación, un capítulo) ese texto se salva como documento propio con el id del
   original y una nota. Un documento que solo contiene un fragmento útil (una genealogía al final de unas
   pruebas de escritura) se queda con el fragmento. Cuando dos textos suyos casi iguales tratan lo mismo,
   se pueden fusionar en uno con secciones ("haz trampa y fusiónalo"), anotándolo. Lo de autoría dudosa se
   deja con `AUTORÍA A CONFIRMAR` al principio de `notas`.
3. **Crear o completar la obra**: `md/<Obra>/_carpeta.md` con `id` (siguiente Cnn), `titulo`, `criterio`
   (qué va en la obra, para las búsquedas futuras) y `notas`. Nombre de obra en la lengua que toque, sin
   chocar con el nombre de ningún documento de dentro.
4. **Mover cada documento** con su `img/` (copiar la carpeta `img` entera, nunca solo el `index.md`: así se
   perdieron imágenes una vez), con **cabecera mínima** `id`, `titulo`, `notas`. En `notas`: qué es, fecha
   y firma, qué versiones había y cuál se eligió, qué se quitó (índices de páginas, notas a terceros,
   pies de foto sin foto) y las dudas de autoría.
5. **Formato**, con un script de un solo uso sobre el grupo y revisión manual después:
   - `# Título` igual al `titulo`; la línea de título original del texto se quita si repite el título.
   - Secciones `##` y `###` para los apartados (negritas sueltas, líneas en mayúsculas, apartados numerados);
     no convertir en título las listas, vocabularios ni frases largas. Pies de foto y firmas en cursiva.
   - Poemas en verso: cada verso con dos espacios finales, sin párrafo entre versos. Prosa en párrafos.
     Diálogos y listas cortas, una línea por réplica.
   - Imágenes en párrafo propio, cada una en su sitio; en las maquetas con foto y texto, la foto encima.
   - Quitar: líneas vacías de relleno, espacios duros, espacios dobles, negritas o cursivas envolventes de
     párrafo o de documento entero, `<span>`, `<u>` (a negrita), `<sup>`, citas `>` que no son citas,
     índices de páginas, referencias del tipo "Foto R-47" y notas dirigidas a terceros (van a `notas`).
   - Las comillas angulares de la autora (`<...>`, `<<...>>`) se dejan escapadas (`\<`), si no markdown las
     oculta. Los `\_` de los ejercicios de rellenar se dejan.
   - Errores que ya pasaron y hay que vigilar: espacios dentro de `**` (tratar por bloques `**texto**`, nunca
     con una regex de un solo lado); negritas troceadas `**4**. **TÍTULO**` que hay que recomponer; el `<u>`
     convertido a negrita que luego se toma por título; líneas largas que pandoc marcó como `#`; el título
     repetido bajo el H1; referencias de foto partidas por una línea de puntos.
6. **Nombres de carpeta y `titulo`**: mayúscula solo al inicio y en nombres propios, con acentos, sin números,
   puntos ni "Paquita" de los nombres de fichero, en la lengua del texto y coherentes con el contenido.
7. **Borrar de `inprocess/`** las versiones usadas y las descartadas de ese grupo, y las carpetas que queden
   vacías. Regenerar índices, `python3 tools/comprueba.py` hasta que diga "md/ correcto", y resumir al
   usuario: qué entra y de qué versión, qué se borró, qué se quedó fuera y por qué, y qué queda a su decisión.
8. Commit y push solo cuando el usuario lo pide ("Haz el commit y push"), uno por obra.

### 4. Fotos que faltan

Si un texto cita fotos que no están (referencias "Foto R-nn", pies sin imagen), buscarlas solo si el usuario
lo autoriza, en `../franciscabacket/multimedia/image/`. Recortar las maquetas a la foto (`convert -shave
-trim` y, si el trim se come el negro, `-crop` fijo) y guardarlas en `img/` con un nombre que diga cuál es.

## Normas de md/ (dictadas por el usuario)

- `md/` es la lista de **obras**: una carpeta por obra con `_carpeta.md` (id, titulo, criterio, notas) y un
  `INDICE.md` generado. Dentro, una carpeta por **documento** con `index.md` y opcionalmente `img/`. Nada más.
- **Identificador canónico** de un documento: su ruta `md/<obra>/<documento>`. Además lleva `id` numérico fijo.
- **Todas las imágenes de `img/` están enlazadas** y todo enlace existe; si no, es un error.
- Los documentos de una obra **comparten estilo** y tienen título y nombre coherentes con el contenido.
- Lo que pasa a `md/` se **regulariza** y se **retira de `inprocess/`**. No puede estar en los dos sitios.
- `python3 tools/comprueba.py` verifica todo esto y sale con error si algo falla. Ejecutarlo tras cualquier
  cambio en `md/`, junto con `python3 tools/indice.py`.

## Cómo trabajar aquí

- **Esperar instrucciones.** No montar pipelines ni estructura de site por adelantado. No automatizar sin
  que lo pida; los scripts de un solo uso para formatear un grupo sí están aceptados.
- **Leer antes de decidir.** El formato no dice la autoría, el nombre del fichero no dice el contenido y
  ningún score automático separa lo suyo de lo ajeno.
- **No borrar por cuenta propia** fuera de lo que el procedimiento establece (versiones descartadas de un
  grupo que se pasa a `md/`). Los descartes generales los hace el usuario o los pide.
- **No buscar candidatos en `../franciscabacket/` ni en `../franciscapublicaciones/`**. Los documentos
  entran solo por `raw/`. Las carpetas hermanas sirven para recuperar algo concreto (imágenes perdidas,
  fotos citadas) cuando el usuario lo autoriza.
- Al reorganizar, **mover carpetas enteras** (`index.md` + `img/`).

## Estructura y herramientas

```
raw/                 bandeja de entrada, ignorada por git salvo .gitkeep. Se vacía tras convertir.
inprocess/<ruta>/<nombre>/  un documento por carpeta, misma jerarquía que raw/. Cabecera completa
                     (id, titulo, origen, formato, caracteres, imagenes, interesa, notas). Si dos ficheros
                     del mismo directorio compartían nombre, la carpeta lleva la extensión: "El camí (txt)".
md/<obra>/<doc>/     los seleccionados. Cabecera mínima (id, titulo, notas).
_carpeta.md          en cada carpeta que agrupa documentos: id "Cnn", titulo, criterio (en md/), notas.
INDICE.md            generados por tools/indice.py en inprocess/, md/ y cada obra. No editar a mano.
tools/convierte.py   raw/ -> inprocess/. Sin rutas no hace nada; --todo lo recorre entero; --forzar regenera
                     lo de inprocess/ (nunca lo de md/). Reconoce cada documento por `origen`.
tools/indice.py      regenera los índices y crea los _carpeta.md que falten (id Cnn siguiente).
tools/comprueba.py   comprueba las normas de md/.
```

Pandoc está en `~/.local/bin/pandoc` (3.6.4, binario descargado). LibreOffice 7.3 en `/usr/bin/soffice`;
los doc y odt pasan por LibreOffice a docx en un temporal y luego por pandoc. `tools/imagen_simple.lua`
quita el tamaño a las imágenes para que pandoc las escriba en markdown y no en HTML.

Git: `main` en `git@github.com:jtpadilla/franciscaineditos.git`. Commits con el formato acordado,
solo cuando el usuario lo pide.
