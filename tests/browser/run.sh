#!/usr/bin/env bash
# Drives the real app in headless Chrome: editing under the local server, then read-only (file + static server).
# Works on a migrated copy of vault/ in a temp dir; your vault and site/ are never touched.
# Needs Node 22+ and Google Chrome.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="${SHOTS:-/tmp/lpt-browser}"
PY="$ROOT/.venv/bin/python"
rm -rf "$WORK" && mkdir -p "$WORK/site"
cp -R "$ROOT/vault" "$WORK/vault"
{ echo "vault_path: $WORK/vault"; sed -n '/^domain_weights/,/^default_weight/p' "$ROOT/config.yaml" | grep -v default_weight; } > "$WORK/config.yaml"
export LPT_CONFIG="$WORK/config.yaml" SHOTS="$WORK" VAULT="$WORK/vault" SITE="$WORK/site"
"$ROOT/.venv/bin/lpt" migrate >/dev/null
# the scenario starts from nothing in progress, whatever the real vault holds today
(cd "$ROOT" && "$PY" -c "
from cli import items as it
for p in it.item_paths('$WORK/vault').values():
    page = it.Page(p)
    page.set('state', 'collected')
    for k in ('picked', 'done', 'dropped', 'planned'): page.remove(k)
    page.sections = [s for s in page.sections if s[0] != 'Time']
    page.save()
")
# a throwaway git repo + bare remote so the Save button has somewhere to push
git -C "$WORK" init -q -b main && git -C "$WORK" config user.email t@example.com && git -C "$WORK" config user.name Test
git init -q --bare -b main "$WORK/remote.git" && git -C "$WORK" remote add origin "$WORK/remote.git"
printf 'site/\nchrome-prof/\nremote.git/\nstatic/\n*.png\n*.log\nconfig.yaml\n' > "$WORK/.gitignore"
git -C "$WORK" add -A && git -C "$WORK" commit -qm init && git -C "$WORK" push -q origin HEAD:main

for p in 8799 8811; do
  if curl -s -o /dev/null "http://127.0.0.1:$p/"; then echo "Port $p is already in use; stop that server first" >&2; exit 2; fi
done

cd "$ROOT"
"$PY" -c "
from pathlib import Path
from cli.server import make_server
from cli.build_graph import build_site, load_meta
build = lambda: build_site('$WORK/vault', '$WORK/site', load_meta('$WORK/config.yaml'))
build()
make_server(Path('$WORK/vault'), Path('$WORK/site'), rebuild=build, port=8799, debounce=0.3, save_to=('origin', 'main')).serve_forever()
" >"$WORK/server.log" 2>&1 &
API=$!
trap 'kill $API ${STATIC:-} 2>/dev/null || true' EXIT
for _ in $(seq 50); do curl -sf http://127.0.0.1:8799/api/ping >/dev/null && break; sleep 0.2; done
curl -sf http://127.0.0.1:8799/api/ping >/dev/null || { echo "Server didn't start:" >&2; cat "$WORK/server.log" >&2; exit 2; }

cd "$ROOT/tests/browser"
status=0
echo "== editing (lpt serve)"
BASE=http://127.0.0.1:8799/ node scenario.mjs || status=1
sleep 1  # let the debounced rebuild land so the read-only copy has the edits
mkdir -p "$WORK/static" && cp "$WORK/site/index.html" "$WORK/static/"
"$PY" -m http.server 8811 --bind 127.0.0.1 --directory "$WORK/static" >/dev/null 2>&1 &
STATIC=$!
sleep 0.5
echo "== read-only (file, and a static server like GitHub Pages)"
STATIC_BASE=http://127.0.0.1:8811/ node ro.mjs || status=1
echo "Screenshots in $WORK"
exit $status
