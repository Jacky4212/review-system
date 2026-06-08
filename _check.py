import json, re
with open(r'D:\code\cherry studio\复习\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
m = re.search(r'const D = ({.*?});', c, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    th = d['radiochemistry']['tH']
    parts = th.split('<div class="ti">')
    with open(r'D:\code\cherry studio\复习\_terms_output.txt', 'w', encoding='utf-8') as f:
        f.write(f'Term groups count: {th.count("tg-title")}\n')
        f.write(f'Term items: {len(parts)-1}\n\n')
        for p in parts[1:]:
            term = re.search(r'<span class="ti-term">([^<]+)</span>', p)
            defn = re.search(r'<span class="ti-def">([^<]+)</span>', p)
            if term and defn:
                f.write(f'=== {term.group(1)} ===\n{defn.group(1)}\n\n')
    # Check topic content for duplicates
    tp = d['radiochemistry']['tpH']
    all_pages = {}
    for tname, html in tp.items():
        pages = re.findall(r'第 (\d+) 页', html)
        for p in pages:
            all_pages.setdefault(tname, []).append(p)
    print('Topic content page counts:')
    for t, plist in all_pages.items():
        pset = set(plist)
        if len(plist) != len(pset):
            print(f'  DUPLICATE: {t}: {len(plist)} total, {len(pset)} unique')
        else:
            print(f'  OK: {t}: {len(plist)} pages')
