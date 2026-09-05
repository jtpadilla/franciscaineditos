#!/usr/bin/env python3
"""Regenera INDICE.md en inprocess/ y en md/ a partir de las cabeceras de sus index.md.

Las carpetas que agrupan documentos (todas menos las de documento y las img/) llevan
un fichero _carpeta.md con cabecera propia (id "C01", "C02"..., titulo, notas). Si a una
carpeta le falta, este script se lo crea con el siguiente id libre.

Uso: python3 tools/indice.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIRS = [RAIZ / "inprocess", RAIZ / "md"]


def cabecera(p: Path) -> dict:
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---\n"):
        return {}
    fm = t[4:].split("\n---\n", 1)[0]
    meta = {}
    for linea in fm.splitlines():
        if ":" in linea:
            k, v = linea.split(":", 1)
            v = v.strip()
            try:
                meta[k.strip()] = json.loads(v)
            except json.JSONDecodeError:
                meta[k.strip()] = v
    return meta


def carpetas_de(base: Path) -> list[Path]:
    """Carpetas que agrupan documentos: las que no son de documento ni img/."""
    out = []
    for d in sorted(base.rglob("*"), key=lambda p: str(p).lower()):
        if d.is_dir() and d.name != "img" and not (d / "index.md").exists() and "img" not in d.relative_to(base).parts:
            out.append(d)
    return out


def asegura_ids_carpetas():
    """Crea _carpeta.md donde falte, con el siguiente id C.. libre (común a inprocess/ y md/)."""
    usados = []
    pendientes = []
    for base in DIRS:
        if not base.is_dir():
            continue
        for d in carpetas_de(base):
            f = d / "_carpeta.md"
            if f.exists():
                i = str(cabecera(f).get("id", ""))
                if i.startswith("C") and i[1:].isdigit():
                    usados.append(int(i[1:]))
            else:
                pendientes.append(f)
    n = max(usados, default=0)
    for f in pendientes:
        n += 1
        f.write_text(f'---\nid: "C{n:02d}"\ntitulo: {json.dumps(f.parent.name, ensure_ascii=False)}\ncriterio: ""\nnotas: ""\n---\n', encoding="utf-8")
        print(f"nueva carpeta C{n:02d}: {f.parent.relative_to(RAIZ)}")


def genera(MD: Path):
    docs = [(p.parent.relative_to(MD), cabecera(p)) for p in MD.rglob("index.md")]
    carps = [(d.relative_to(MD), cabecera(d / "_carpeta.md")) for d in carpetas_de(MD)]
    filas = sorted([(c, "carpeta", m) for c, m in carps] + [(c, "doc", m) for c, m in docs],
                   key=lambda f: (str(f[0]).lower().split("/")))
    n_si = sum(1 for _, t, m in docs_only(filas) if str(m.get("interesa", "")).lower().startswith("s"))
    n_no = sum(1 for _, t, m in docs_only(filas) if str(m.get("interesa", "")).lower() == "no")
    n = len(docs)
    seleccion = MD.name == "md"
    out = [f"# Índice de {MD.name}/", ""]
    if seleccion:
        out += [f"{n} documentos seleccionados en {len(carps)} carpetas.", "",
                "Se regenera con `python3 tools/indice.py`. Edita las cabeceras (`id`, `titulo`, `notas`) de cada "
                "`index.md` y `_carpeta.md`, no esta tabla.", "",
                "| Id | Documento | Título | Notas |", "|---|---|---|---|"]
    else:
        out += [f"{n} documentos en {len(carps)} carpetas. Interesan: {n_si}. Descartados: {n_no}. Sin revisar: {n - n_si - n_no}.", "",
                "Se regenera con `python3 tools/indice.py`. Edita las cabeceras de cada `index.md` y `_carpeta.md`, no esta tabla. "
                "Los ids son fijos: `001`... para documentos, `C01`... para carpetas.", "",
                "| Id | Documento | Título | Formato | Car. | Img | Interesa | Notas |",
                "|---|---|---|---|---|---|---|---|"]
    for ruta, tipo, m in filas:
        url = str(ruta)
        if tipo == "carpeta":
            n_docs = sum(1 for r, t, _ in filas if t == "doc" and str(r).startswith(str(ruta) + "/"))
            if seleccion:
                out.append(f"| **{m.get('id', '')}** | **[{ruta}/](<{url}/_carpeta.md>)** ({n_docs} docs) | **{m.get('titulo', '')}** | {m.get('notas', '')} |")
            else:
                out.append(f"| **{m.get('id', '')}** | **[{ruta}/](<{url}/_carpeta.md>)** | **{m.get('titulo', '')}** | carpeta | {n_docs} docs | | | {m.get('notas', '')} |")
        elif seleccion:
            out.append(f"| {m.get('id', '')} | [{ruta}](<{url}/index.md>) | {m.get('titulo', '')} | {m.get('notas', '')} |")
        else:
            out.append(f"| {m.get('id', '')} | [{ruta}](<{url}/index.md>) | {m.get('titulo', '')} | {m.get('formato', '')} | "
                       f"{m.get('caracteres', '')} | {m.get('imagenes', '')} | {m.get('interesa', '')} | {m.get('notas', '')} |")
    (MD / "INDICE.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{n} documentos y {len(carps)} carpetas en {MD.name}/INDICE.md")


def indices_por_carpeta(MD: Path):
    """En md/, un INDICE.md dentro de cada carpeta con lo que cuelga directamente de ella."""
    for d in carpetas_de(MD):
        m = cabecera(d / "_carpeta.md")
        filas = []
        for h in sorted(d.iterdir(), key=lambda p: p.name.lower()):
            if not h.is_dir() or h.name == "img":
                continue
            if (h / "index.md").exists():
                c = cabecera(h / "index.md")
                filas.append(f"| {c.get('id', '')} | [{h.name}](<{h.name}/index.md>) | {c.get('titulo', '')} | {c.get('notas', '')} |")
            elif (h / "_carpeta.md").exists():
                c = cabecera(h / "_carpeta.md")
                n = len(list(h.rglob("index.md")))
                filas.append(f"| **{c.get('id', '')}** | **[{h.name}/](<{h.name}/INDICE.md>)** ({n} docs) | **{c.get('titulo', '')}** | {c.get('notas', '')} |")
        arriba = "../INDICE.md"
        out = [f"# {m.get('titulo', d.name)}", "", f"Id **{m.get('id', '')}**. {m.get('notas', '')}".rstrip(), "",
               f"**Qué va en esta obra:** {m.get('criterio', '') or '(sin criterio todavía: rellenar `criterio` en _carpeta.md)'}", "",
               f"[Índice superior]({arriba})", "",
               "| Id | Documento | Título | Notas |", "|---|---|---|---|"] + filas
        (d / "INDICE.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def docs_only(filas):
    return [f for f in filas if f[1] == "doc"]


def main():
    asegura_ids_carpetas()
    for d in DIRS:
        if d.is_dir():
            genera(d)
    indices_por_carpeta(RAIZ / "md")


if __name__ == "__main__":
    main()
