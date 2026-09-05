#!/usr/bin/env python3
"""Convierte todo lo que hay en raw/ a markdown en inprocess/, un documento por carpeta.

    raw/<ruta>/<nombre>.<ext>  ->  inprocess/<ruta>/<nombre>/index.md  (+ img/ si hay imágenes)

- docx: pandoc directo.
- doc, odt, rtf: primero LibreOffice -> docx (en un directorio temporal), luego pandoc.
- txt: se copia tal cual.
- Imágenes wmf/emf se convierten a png con LibreOffice.

No toca raw/. Salta todo documento cuyo `origen` ya aparezca en la cabecera de algún
index.md de inprocess/ o de md/, aunque el usuario haya renombrado o movido la carpeta
(para no pisar lo que haya editado ni duplicar lo ya seleccionado). Con --forzar
regenera los de inprocess/; los que están en md/ no se regeneran nunca.

Uso: python3 tools/convierte.py [--forzar] ruta-dentro-de-raw ...
     python3 tools/convierte.py --todo    (todo raw/; sin --todo y sin rutas no hace nada)
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "raw"
MD = RAIZ / "inprocess"
SELECCIONADOS = RAIZ / "md"
PANDOC = shutil.which("pandoc") or str(Path.home() / ".local/bin/pandoc")
FORMATOS = {".docx", ".doc", ".odt", ".rtf", ".txt"}


def a_docx(origen: Path, tmp: Path) -> Path:
    subprocess.run(["soffice", "--headless", "--convert-to", "docx", "--outdir", str(tmp), str(origen)],
                   check=True, capture_output=True)
    return tmp / (origen.stem + ".docx")


def wmf_a_png(img: Path) -> Path:
    subprocess.run(["soffice", "--headless", "--convert-to", "png", "--outdir", str(img.parent), str(img)],
                   check=True, capture_output=True)
    png = img.with_suffix(".png")
    if png.exists():
        img.unlink()
        return png
    return img


def cabeceras_existentes() -> tuple[dict[str, Path], dict[str, str], int]:
    """Lee todos los index.md de inprocess/ y md/. Devuelve origen -> carpeta,
    origen -> id, y el mayor id usado."""
    carpetas, ids, mayor = {}, {}, 0
    for base in (SELECCIONADOS, MD):
        for idx in base.rglob("index.md"):
            fm = idx.read_text(encoding="utf-8").split("\n---\n", 1)[0]
            m = re.search(r'^origen: (".*")$', fm, re.M)
            i = re.search(r'^id: "(\d+)"$', fm, re.M)
            if m:
                o = json.loads(m.group(1))
                carpetas[o] = idx.parent
                if i:
                    ids[o] = i.group(1)
            if i:
                mayor = max(mayor, int(i.group(1)))
    return carpetas, ids, mayor


def convierte(origen: Path, destino: Path, forzar: bool, existentes: dict[str, Path], id_doc: str) -> dict | None:
    rel = str(origen.relative_to(RAW))
    previa = existentes.get(rel)
    if previa is not None:
        if SELECCIONADOS in previa.parents:
            return None            # ya seleccionado en md/: nunca se toca
        if not forzar:
            return None
        shutil.rmtree(previa)
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    ext = origen.suffix.lower()
    if ext == ".txt":
        raw = origen.read_bytes()
        for enc in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                texto = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        texto = texto.replace("\r\n", "\n")
    else:
        with tempfile.TemporaryDirectory() as t:
            docx = origen if ext == ".docx" else a_docx(origen, Path(t))
            r = subprocess.run([PANDOC, str(docx), "-t", "gfm", "--wrap=none", "--extract-media=.",
                               "--lua-filter", str(RAIZ / "tools/imagen_simple.lua")],
                               cwd=destino, capture_output=True, text=True)
            if r.returncode != 0:
                shutil.rmtree(destino)
                print(f"  FALLO pandoc: {origen}: {r.stderr.strip()[:200]}", file=sys.stderr)
                return None
            texto = r.stdout
        media = destino / "media"
        if media.exists():
            media.rename(destino / "img")
            texto = texto.replace("](./media/", "](img/").replace("](media/", "](img/")
            texto = re.sub(r'<img src="(?:\./)?media/([^"]+)"[^>]*/?>', r"![](img/\1)", texto)
            # imágenes pegadas al texto -> línea propia
            out = []
            for l in texto.split("\n"):
                imgs = re.findall(r"!\[[^\]]*\]\([^)]*\)", l)
                if imgs and l.strip() not in imgs:
                    resto = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", l).strip()
                    for i in imgs: out += [i, ""]
                    out.append(resto)
                elif len(imgs) > 1:
                    for i in imgs: out += [i, ""]
                else:
                    out.append(l)
            texto = "\n".join(out)
            for f in list((destino / "img").iterdir()):
                if f.suffix.lower() in (".wmf", ".emf"):
                    nuevo = wmf_a_png(f)
                    texto = texto.replace(f"img/{f.name}", f"img/{nuevo.name}")
    n_img = len(list((destino / "img").iterdir())) if (destino / "img").exists() else 0
    cuerpo = re.sub(r"\n{3,}", "\n\n", texto).strip() + "\n"
    caracteres = len(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", cuerpo))
    meta = {
        "id": id_doc,
        "titulo": origen.stem,
        "origen": str(origen.relative_to(RAW)),
        "formato": ext[1:],
        "caracteres": caracteres,
        "imagenes": n_img,
        "interesa": "",
        "notas": "",
    }
    fm = "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items()) + "\n---\n\n"
    (destino / "index.md").write_text(fm + cuerpo, encoding="utf-8")
    return meta


def nombres_destino(ficheros: list[Path]) -> dict[Path, str]:
    """Nombre de carpeta = nombre sin extensión; si dos ficheros del mismo
    directorio comparten nombre, se añade la extensión entre paréntesis."""
    por_stem: dict[tuple, list[Path]] = {}
    for f in ficheros:
        por_stem.setdefault((f.parent, f.stem), []).append(f)
    out = {}
    for (_, stem), fs in por_stem.items():
        for f in fs:
            out[f] = stem if len(fs) == 1 else f"{stem} ({f.suffix[1:].lower()})"
    return out


def main(argv):
    forzar = "--forzar" in argv
    rutas = [a for a in argv if not a.startswith("--")]
    if not rutas and "--todo" not in argv:
        print("Indica rutas dentro de raw/ o usa --todo para convertir todo.", file=sys.stderr)
        sys.exit(1)
    base = [RAW / r for r in rutas] if rutas else [RAW]
    ficheros = sorted(f for b in base for f in (b.rglob("*") if b.is_dir() else [b])
                      if f.is_file() and f.suffix.lower() in FORMATOS)
    nombres = nombres_destino(ficheros)
    existentes, ids, mayor = cabeceras_existentes()
    hechos = saltados = 0
    for f in ficheros:
        destino = MD / f.parent.relative_to(RAW) / nombres[f]
        rel = str(f.relative_to(RAW))
        if rel in ids:
            id_doc = ids[rel]              # conserva el id aunque se regenere con --forzar
        else:
            mayor += 1
            id_doc = f"{mayor:03d}"
        meta = convierte(f, destino, forzar, existentes, id_doc)
        if meta is None:
            saltados += 1
        else:
            hechos += 1
            print(f"[{meta['id']}] {meta['origen']}  ->  {destino.relative_to(RAIZ)}  ({meta['caracteres']} car., {meta['imagenes']} img)")
    print(f"\n{hechos} convertidos, {saltados} saltados o fallidos.")


if __name__ == "__main__":
    main(sys.argv[1:])
