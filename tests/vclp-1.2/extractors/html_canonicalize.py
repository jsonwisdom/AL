#!/usr/bin/env python3
"""VCLP 1.2 HTML Canonical Extractor - Fixed tree traversal"""

import sys
import hashlib
import unicodedata
import re
import html5lib

def get_text_from_node(node):
    """Extract text from html5lib tree node (using simple tree builder)"""
    texts = []
    
    # Skip script/style tags
    tag = node.get('tag', '') if hasattr(node, 'get') else ''
    if tag in ('script', 'style', 'noscript', 'template', 'head'):
        return ''
    
    # Get text content
    if hasattr(node, 'text') and node.text:
        texts.append(node.text)
    
    # Process children
    if hasattr(node, 'children'):
        for child in node.children:
            texts.append(get_text_from_node(child))
            if hasattr(child, 'tail') and child.tail:
                texts.append(child.tail)
    
    # Block element separators
    if tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
               'li', 'br', 'hr', 'section', 'article', 'nav',
               'header', 'footer', 'main', 'aside', 'blockquote'):
        if texts and not texts[-1].endswith('\n'):
            texts.append('\n')
    
    return ''.join(texts)

def canonicalize_html(raw_bytes):
    """Return (canonical_bytes, status)"""
    
    # Strict UTF-8 decode
    try:
        html_str = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return None, "TAINTED: invalid UTF-8"
    
    # Parse with html5lib (simple tree builder - more compatible)
    try:
        parser = html5lib.HTMLParser()
        doc = parser.parse(html_str)
    except Exception as e:
        return None, f"TAINTED: parse error - {e}"
    
    # Find body
    body = None
    if hasattr(doc, 'children'):
        for child in doc.children:
            if hasattr(child, 'get') and child.get('tag') == 'html':
                for grandchild in child.children:
                    if hasattr(grandchild, 'get') and grandchild.get('tag') == 'body':
                        body = grandchild
                        break
    
    if body is None:
        # Fallback to whole document
        body = doc
    
    # Extract text
    raw_text = get_text_from_node(body)
    
    # Whitespace collapse
    collapsed = re.sub(r'\s+', ' ', raw_text).strip()
    
    # NFC normalize
    normalized = unicodedata.normalize('NFC', collapsed)
    
    # Encode to UTF-8 no BOM
    output_bytes = normalized.encode('utf-8')
    
    return output_bytes, "OK"

def main():
    if len(sys.argv) != 2:
        print("Usage: html_canonicalize.py <html_file>", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1], 'rb') as f:
        html_bytes = f.read()
    
    canonical_bytes, status = canonicalize_html(html_bytes)
    
    if canonical_bytes is None:
        print(status)
        sys.exit(1)
    
    hash_hex = hashlib.sha256(canonical_bytes).hexdigest()
    print(f"sha256:{hash_hex}")
    print(f"STATUS: {status}", file=sys.stderr)
    
    # Debug: show extracted text preview
    preview = canonical_bytes[:100].decode('utf-8', errors='replace')
    print(f"PREVIEW: {preview}", file=sys.stderr)

if __name__ == '__main__':
    main()
