import json, re
with open(r'D:\code\cherry studio\复习\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
m = re.search(r'const D = ({.*?});', c, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    tp = d['radiochemistry']['tpH']
    for et in d['radiochemistry']['examTopics']:
        html = tp.get(et['topic'], '')
        pages = re.findall(r'第 (\d+) 页', html)
        name = et['topic']
        if pages:
            unique = len(set(pages))
            print(f'  {name}: {unique} pages')
        else:
            print(f'  {name}: EMPTY')
