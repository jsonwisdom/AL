#!/usr/bin/env python3
"""VCLP 1.2 HTML Canonical Extractor - LAB ONLY.
Uses html5lib with etree treebuilder (tag/text/tail attributes).
No verifier integration. No CI enforcement.
"""
import hashlib
import re
import sys
import unicodedata
import html5lib
from html5lib import treebuilders

SKIP_TAGS = {"script", "style", "noscript", "template", "head"}
BLOCK_TAGS = {
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "br", "hr", "section", "article", "nav",
    "header", "footer", "main", "aside", "blockquote"
}

def strip_namespace(tag):
    """Remove XML namespace prefix if present."""
    return tag.split('}')[-1] if '}' in tag else tag

def extract_text(node):
    """Extract text from etree node (tag/text/tail attributes)."""
    parts = []
    
    # Get tag name without namespace
    tag = strip_namespace(node.tag) if hasattr(node, 'tag') else None
    
    # Skip non-content elements
    if tag in SKIP_TAGS:
        return ""
    
    # Add node's own text
    if hasattr(node, 'text') and node.text:
        parts.append(node.text)
    
    # Process children
    for child in node:
        parts.append(extract_text(child))
    
    # Add tail text (text after this element)
    if hasattr(node, 'tail') and node.tail:
        parts.append(node.tail)
    
    # Add block separators
    if tag in BLOCK_TAGS or tag == 'br':
        if parts and not parts[-1].endswith('\n'):
            parts.append('\n')
    
    return ''.join(parts)

def canonicalize_html(raw_bytes):
    """Return (canonical_bytes, status) where status is OK or TAINTED."""
    
    # Strict UTF-8 decode
    try:
        html_str = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return None, "TAINTED: invalid UTF-8"
    
    # Parse with html5lib using etree builder
    try:
        parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))
        doc = parser.parse(html_str)
    except Exception as e:
        return None, f"TAINTED: parse error - {e}"
    
    # Find body element
    body = None
    for elem in doc.iter():
        tag = strip_namespace(elem.tag) if hasattr(elem, 'tag') else None
        if tag == 'body':
            body = elem
            break
    
    root = body if body is not None else doc
    
    # Extract text
    raw_text = extract_text(root)
    
    # Normalize line endings
    raw_text = raw_text.replace('\r\n', '\n').replace('\r', '\n')
    
    # NFC normalize
    raw_text = unicodedata.normalize('NFC', raw_text)
    
    # Lab policy: collapse whitespace runs to single space
    collapsed = re.sub(r'\s+', ' ', raw_text).strip()
    
    canonical_bytes = collapsed.encode('utf-8')
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
