#!/usr/bin/env python3
"""Fix PUA garbled chars in extracted text files and verify HTML."""
import os

PUA_MAP = {
    0xF0B4: '×', 0xF02D: '−', 0xF0AE: '→', 0xF0AF: '↓',
    0xF075: 'v',  0xF0A3: '≤', 0xF0AD: '↑', 0xF0BB: '≠',
    0xF0B9: '≠',  0xF0BE: '—', 0xF0C5: '⊕', 0xF0D7: '·',
    0xF0DB: '⇔',  0xF06D: 'μ', 0xF057: 'Ω', 0xF074: 'τ',
    0xF0A5: '∞',  0xF0E0: '→', 0xF03E: '>',  0xF0B3: '≥',
    0xF0BC: 'n',  0xF0E5: 'Σ', 0xF044: 'Δ', 0xF065: 'ε',
    0xF06C: 'λ',  0xF068: '◆', 0xF098: '■', 0xF02B: '+',
    0xF0A2: '′',  0xF02F: '/',
}

# Fix extracted .txt files
extract = "D:/code/cherry studio/复习/数字电子技术/提取内容"
total = 0
for fname in os.listdir(extract):
    if not fname.endswith('.txt'):
        continue
    path = os.path.join(extract, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    fixes = 0
    result = []
    for ch in content:
        cp = ord(ch)
        if cp in PUA_MAP:
            result.append(PUA_MAP[cp])
            fixes += 1
        else:
            result.append(ch)
    if fixes > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(''.join(result))
        print("提取内容/%s: 修复 %d 处" % (fname, fixes))
        total += fixes

print("\n共修复 %d 处PUA乱码字符" % total)
print()

# Now also fix generate_chapters.py in case it has PUA chars
gen_py = "D:/code/cherry studio/复习/数字电子技术/generate_chapters.py"
with open(gen_py, 'r', encoding='utf-8') as f:
    content = f.read()
fixes = 0
result = []
for ch in content:
    cp = ord(ch)
    if cp in PUA_MAP:
        result.append(PUA_MAP[cp])
        fixes += 1
    else:
        result.append(ch)
if fixes > 0:
    with open(gen_py, 'w', encoding='utf-8') as f:
        f.write(''.join(result))
    print("generate_chapters.py: 修复 %d 处" % fixes)
else:
    print("generate_chapters.py: 无PUA字符")
