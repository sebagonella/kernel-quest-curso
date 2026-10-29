"""Confere os links internos e as imagens de todos os .md do repositório."""

import re
import sys
from pathlib import Path

raiz = Path(__file__).resolve().parents[2]
falhas = []
for md in sorted(raiz.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for alvo in re.findall(r"\]\(([^)#\s]+)", md.read_text(encoding="utf-8")):
        if not re.match(r"[a-z]+:", alvo) and not (md.parent / alvo).exists():
            falhas.append(f"{md.relative_to(raiz)}: link quebrado -> {alvo}")
print("\n".join(falhas) or "[OK] links e imagens")
sys.exit(1 if falhas else 0)
