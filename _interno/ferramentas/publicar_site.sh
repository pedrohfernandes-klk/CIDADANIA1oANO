#!/usr/bin/env bash
# Gera o site dos alunos (docs/) e publica-o no ramo gh-pages (GitHub Pages).
# Uso, na raiz do repositório:  bash _interno/ferramentas/publicar_site.sh
# Endereço: https://pedrohfernandes-klk.github.io/CIDADANIA1oANO/
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python3 _interno/ferramentas/gerar_site.py
TMP=$(mktemp -d)
git fetch -q origin gh-pages
git worktree add -q "$TMP" origin/gh-pages
rsync -a --delete --exclude .git docs/ "$TMP"/
cd "$TMP"
git add -A
if git diff --cached --quiet; then echo "Site sem alterações."; else
  git commit -q -m "Atualiza o site dos alunos"
  git push -q origin HEAD:gh-pages
  echo "Publicado. O GitHub demora cerca de um minuto a atualizar."
fi
cd - >/dev/null
git worktree remove --force "$TMP"
