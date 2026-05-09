#!/usr/bin/env python3
"""VCLP 1.2 HTML Canonical Extractor - LAB ONLY.
Uses html5lib default DOM treebuilder.
No verifier integration. No CI enforcement.
"""
import hashlib
import re
import sys
import unicodedata
import html5lib
SKIP_TAGS = {"script", "style", "noscript", "template", "head"}
BLOCK_TAGS = {
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "br", "hr", "section", "article", "nav",
    "header", "footer", "main", "aside", "blockquote"
}
def node_name(node):
    return getattr(node, "nodeName", "").lower()
def find_body(node):
    if node_name(node) == "body":
        return node
    for child in getattr(node, "childNodes", []) or []:
        found = find_body(child)
        if found is not None:
            return found
    return None
def extract_text(node):
    node_type = getattr(node, "nodeType", None)
    # TEXT_NODE
    if node_type == 3:
        return getattr(node, "nodeValue", "") or ""
    # ELEMENT_NODE
    if node_type == 1:
        name = node_name(node)
        if name in SKIP_TAGS:
            return ""
        parts = []
        if name == "br":
            parts.append("\n")
        for child in getattr(node, "childNodes", []) or []:
            parts.append(extract_text(child))
        if name in BLOCK_TAGS:
            parts.append("\n")
        return "".join(parts)
    # DOCUMENT or other container nodes
    parts = []
    for child in getattr(node, "childNodes", []) or []:
        parts.append(extract_text(child))
    return "".join(parts)
def canonicalize_html(raw_bytes):
    try:
        html_str = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None, "TAINTED: invalid UTF-8"
    try:
        parser = html5lib.HTMLParser()
        doc = parser.parse(html_str)
    except Exception as exc:
        return None, f"TAINTED: parse error: {exc}"
    body = find_body(doc)
    root = body if body is not None else doc
    raw_text = extract_text(root)
    raw_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    raw_text = unicodedata.normalize("NFC", raw_text)
    # Lab policy: collapse all whitespace to one space for now.
    collapsed = re.sub(r"\s+", " ", raw_text).strip()
    canonical_bytes = collapsed.encode("utf-8")
    return canonical_bytes, "OK"
def main():
    if len(sys.argv) != 2:
        print("Usage: html_canonicalize.py <html_file>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "rb") as fh:
        raw_bytes = fh.read()
    canonical_bytes, status = canonicalize_html(raw_bytes)
    if canonical_bytes is None:
        print(status)
        sys.exit(1)
    digest = hashlib.sha256(canonical_bytes).hexdigest()
    print(f"sha256:{digest}")
    print(f"STATUS: {status}", file=sys.stderr)
    print(f"PREVIEW: {canonical_bytes.decode('utf-8', errors='replace')}", file=sys.stderr)
if __name__ == "__main__":
    main()
