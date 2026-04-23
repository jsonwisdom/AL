#!/usr/bin/env bash
set -euo pipefail
HTML_FILE="${1:-}"
[[ -f "$HTML_FILE" ]] || { echo "Usage: html_to_text.sh <file.html>" >&2; exit 1; }
python3 - "${HTML_FILE}" <<'PY'
from bs4 import BeautifulSoup
from pathlib import Path
import sys, unicodedata, re
html = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")
for tag in soup(["script", "style", "noscript", "meta", "link"]):
    tag.decompose()
text = soup.get_text(" ")
text = unicodedata.normalize("NFC", text)
text = re.sub(r"\s+", " ", text).strip()
print(text)
PY
