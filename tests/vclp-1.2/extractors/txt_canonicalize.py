#!/usr/bin/env python3
"""VCLP 1.2 TXT Canonical Extractor
Strict UTF-8, no replacements, TAINTED on invalid.
"""

import sys
import unicodedata
import hashlib

def canonicalize_txt(raw_bytes):
    """Return (canonical_bytes, status) where status is OK or TAINTED."""
    
    # Step 1: Strip exactly one leading UTF-8 BOM if present
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]
    
    # Step 2: Strict UTF-8 decode -> TAINTED on failure
    try:
        text = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return None, "TAINTED: invalid UTF-8"
    
    # Step 3: Normalize line endings
    # CRLF -> LF, standalone CR -> LF
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    
    # Step 4: Unicode NFC normalization
    text = unicodedata.normalize('NFC', text)
    
    # Step 5: Encode to UTF-8 no BOM
    canonical_bytes = text.encode('utf-8')
    
    return canonical_bytes, "OK"

def main():
    if len(sys.argv) != 2:
        print("Usage: txt_canonicalize.py <txt_file>", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1], 'rb') as f:
        raw_bytes = f.read()
    
    canonical_bytes, status = canonicalize_txt(raw_bytes)
    
    if canonical_bytes is None:
        print(status)
        sys.exit(1)
    
    hash_hex = hashlib.sha256(canonical_bytes).hexdigest()
    print(f"sha256:{hash_hex}")
    print(f"STATUS: {status}", file=sys.stderr)

if __name__ == '__main__':
    main()
