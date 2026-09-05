#!/usr/bin/env python3
"""Comprueba las normas de md/. Cada aviso es un error que hay que corregir.

- Cada documento es md/<obra>/<documento>/index.md, opcionalmente con img/.
- Toda imagen de img/ está enlazada desde el index.md, y todo enlace ![](img/...) existe.
- La cabecera tiene id, titulo y notas (y nada más); el H1 del cuerpo es igual al titulo.
- Cada obra tiene _carpeta.md con id, titulo, criterio y notas; criterio no está vacío.
- No hay ids repetidos entre inprocess/ y md/.

Uso: python3 tools/comprueba.py   (sale con 1 si hay errores)
"""
import json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MD, INP = RAIZ / "md", RAIZ / "inprocess"
errores = []


def cabecera(p: Path) -> dict:
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---\n") or "\n---\n" not in t:
        errores.append(f"{p}: sin cabecera YAML"); return {}
    fm = t[4:].split("\n---\n", 1)[0]
    m = {}
    for l in fm.splitlines():
        if ":" in l:
            k, v = l.split(":", 1)
            try: m[k.strip()] = json.loads(v.strip())
            except json.JSONDecodeError: m[k.strip()] = v.strip()
    return m


def cuerpo(p: Path) -> str:
    return p.read_text(encoding="utf-8").split("\n---\n", 1)[1]


ids = {}
for base in (INP, MD):
    for f in list(base.rglob("index.md")) + list(base.rglob("_carpeta.md")):
        i = str(cabecera(f).get("id", ""))
        if i in ids: errores.append(f"id {i} repetido: {ids[i]} y {f.relative_to(RAIZ)}")
        ids[i] = f.relative_to(RAIZ)

for obra in sorted(d for d in MD.iterdir() if d.is_dir()):
    c = obra / "_carpeta.md"
    if not c.exists():
        errores.append(f"{obra.relative_to(RAIZ)}: falta _carpeta.md"); continue
    m = cabecera(c)
    for k in ("id", "titulo", "criterio", "notas"):
        if k not in m: errores.append(f"{c.relative_to(RAIZ)}: falta el campo {k}")
    if not m.get("criterio"): errores.append(f"{c.relative_to(RAIZ)}: criterio vacío")
    for h in sorted(obra.iterdir()):
        if not h.is_dir(): continue
        idx = h / "index.md"
        if not idx.exists():
            errores.append(f"{h.relative_to(RAIZ)}: carpeta sin index.md (en md/ no hay subcarpetas dentro de una obra)"); continue
        m = cabecera(idx)
        extra = set(m) - {"id", "titulo", "notas"}
        if extra: errores.append(f"{idx.relative_to(RAIZ)}: campos de más en la cabecera: {', '.join(sorted(extra))}")
        for k in ("id", "titulo", "notas"):
            if k not in m: errores.append(f"{idx.relative_to(RAIZ)}: falta el campo {k}")
        cu = cuerpo(idx)
        h1 = re.search(r"^# (.+)$", cu, re.M)
        if not h1: errores.append(f"{idx.relative_to(RAIZ)}: sin título H1")
        elif h1.group(1).strip() != str(m.get("titulo", "")).strip():
            errores.append(f"{idx.relative_to(RAIZ)}: H1 «{h1.group(1)}» distinto de titulo «{m.get('titulo')}»")
        refs = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", cu))
        for r in refs:
            if not (h / r).exists(): errores.append(f"{idx.relative_to(RAIZ)}: enlace roto a {r}")
        img = h / "img"
        if img.exists():
            for f in img.iterdir():
                if f"img/{f.name}" not in refs: errores.append(f"{idx.relative_to(RAIZ)}: imagen sin enlazar img/{f.name}")
        for otra in h.iterdir():
            if otra.is_dir() and otra.name != "img": errores.append(f"{otra.relative_to(RAIZ)}: subcarpeta que no es img/")

if errores:
    print("\n".join(errores)); print(f"\n{len(errores)} errores"); sys.exit(1)
print("md/ correcto")
