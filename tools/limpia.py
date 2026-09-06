"""Limpieza tipográfica de md/ por categorías. No toca palabras, acentos ni ortografía.

Uso: python3 tools/limpia.py A1 [A2 ...] [--aplica]
Sin --aplica solo informa. Solo actúa sobre el cuerpo (después de la cabecera YAML) y salta las
líneas de imagen, de tabla y de cabecera, y las que llevan URL o correo.
"""
import re, sys, glob
from pathlib import Path

def a1(l):
    """Espacios: duros, dobles, finales (salvo verso), dentro de paréntesis y delante de signo."""
    verso = l.endswith("  ") and not l.endswith("   ")
    l = l.replace("\xa0", " ")
    m = re.match(r"^(\s*(?:[-*]|\d+\.)\s+)", l)          # conserva la sangría de lista
    pre, resto = (m.group(1), l[m.end():]) if m else ("", l)
    resto = re.sub(r"(?<=\S)  +(?=\S)", " ", resto)
    resto = re.sub(r"\( +(?=\S)", "(", resto); resto = re.sub(r"(?<=\S) +\)", ")", resto)
    resto = re.sub(r"(?<=\S) +([,;:?!])", r"\1", resto)
    resto = re.sub(r"(?<=\S) +\.(?!\.)", ".", resto)
    resto = resto.rstrip() + ("  " if verso else "")
    return pre + resto

def a2(l):
    """Espacio que falta tras coma entre letras y tras punto ante mayúscula."""
    L = "a-záéíóúàèòíïüçñ"
    l = re.sub(rf"([{L}]),([A-Za-z{L}ÁÉÍÓÚÀÈÒÏÜÇÑ])", r"\1, \2", l)
    l = re.sub(rf"([{L}])\.([A-ZÁÉÍÓÚÀÈÒÏÜÇÑ][{L}])", r"\1. \2", l)
    return l

CATS = {"A1": a1, "A2": a2}

def main():
    cats = [a for a in sys.argv[1:] if a in CATS]; aplica = "--aplica" in sys.argv
    total = 0
    for f in sorted(glob.glob("md/*/*/index.md")):
        t = Path(f).read_text(); cab, cuerpo = t.split("\n---\n", 1)
        out = []; n = 0
        for l in cuerpo.split("\n"):
            if l.startswith(("![", "#", "|")) or "http" in l or "@" in l: out.append(l); continue
            nl = l
            for c in cats: nl = CATS[c](nl)
            if nl != l: n += 1
            out.append(nl)
        if n:
            total += n; print(f"{n:>4}  {f[3:]}")
            if aplica: Path(f).write_text(cab + "\n---\n" + "\n".join(out))
    print(f"\n{total} líneas cambiadas en {' '.join(cats)}{'' if aplica else ' (sin aplicar)'}")

if __name__ == "__main__": main()
