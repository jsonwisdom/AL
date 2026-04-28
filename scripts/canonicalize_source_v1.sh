#!/usr/bin/env bash
set -euo pipefail

SOURCE_FILE="${1:?source file required}"
OUT_FILE="${2:?output file required}"

case "$SOURCE_FILE" in
  *.pdf|*.PDF)
    if ! command -v pdftotext >/dev/null 2>&1; then
      echo "MISSING_DEPENDENCY pdftotext" >&2
      exit 1
    fi
    pdftotext -layout -nopgbrk "$SOURCE_FILE" "$OUT_FILE"
    echo "CANONICALIZE_OK ruleset=gov-pdf-mn-v1"
    ;;
  *.htm|*.html|*.HTM|*.HTML)
    if command -v lynx >/dev/null 2>&1; then
      lynx -dump -nolist "$SOURCE_FILE" > "$OUT_FILE"
      echo "CANONICALIZE_OK ruleset=gov-html-mn-v1 extractor=lynx"
    elif command -v pandoc >/dev/null 2>&1; then
      pandoc "$SOURCE_FILE" -t plain -o "$OUT_FILE"
      echo "CANONICALIZE_OK ruleset=gov-html-mn-v1 extractor=pandoc"
    else
      sed -E 's/<[^>]+>/ /g' "$SOURCE_FILE" \
        | sed 's/&nbsp;/ /g;s/&amp;/\&/g;s/&quot;/"/g;s/&#39;/'"'"'/g' \
        > "$OUT_FILE"
      echo "CANONICALIZE_OK ruleset=gov-html-mn-v1 extractor=sed_fallback"
    fi
    ;;
  *)
    echo "UNSUPPORTED_SOURCE_TYPE file=$SOURCE_FILE" >&2
    exit 1
    ;;
esac
