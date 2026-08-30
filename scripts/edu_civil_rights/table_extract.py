import sys, json, re

if len(sys.argv) != 2:
    sys.stderr.write("usage: table_extract.py INPUT.txt\n")
    sys.exit(64)

text = open(sys.argv[1]).read().splitlines()
rows = []

for line in text:
    if re.search(r'\d', line) and ',' in line:
        rows.append(line)

json.dump({"rows": rows}, sys.stdout, indent=2)
