import json, re
with open(r'D:\code\cherry studio\复习\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
m = re.search(r'const D = ({.*?});', c, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    th = d['radiochemistry']['tH']
    parts = th.split('<div class="ti">')
    print(f"Terms: {len(parts)-1}")
    for p in parts[1:]:
        term = re.search(r'<span class="ti-term">([^<]+)</span>', p)
        defn = re.search(r'<span class="ti-def">([^<]+)</span>', p)
        if term and defn:
            t = term.group(1)
            d = defn.group(1)[:60]
            print(f"  [{t}] {d}...")
