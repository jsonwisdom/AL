#!/usr/bin/env python3
# ALMS verifier script (see manifest)
import argparse, hashlib, pathlib

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()

p=argparse.ArgumentParser();p.add_argument('--pdf',required=True);p.add_argument('--text',required=True);a=p.parse_args()
pdf=pathlib.Path(a.pdf);txt=pathlib.Path(a.text)
print('PDF HASH:',sha256_bytes(pdf.read_bytes()))
print('TEXT HASH:',sha256_bytes(txt.read_bytes()))
print('MATCH?',sha256_bytes(pdf.read_bytes())==sha256_bytes(txt.read_bytes()))
