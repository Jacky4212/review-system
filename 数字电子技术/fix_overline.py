#!/usr/bin/env python3
"""Fix NOT notation: ~X → X̅ (combining overline) in HTML files."""
import os

OV = '̅'  # combining overline

base = "D:/code/cherry studio/复习/数字电子技术"

# Specific replacements for each file
fixes = {
    'ch02.html': [
        # De Morgan's law - use CSS overline for multi-char expressions
        ('摩根定律：~(A·B)=~A+~B，~(A+B)=~A·~B',
         '摩根定律：<span style="text-decoration:overline">(A·B)</span>=<span style="text-decoration:overline">A</span>+<span style="text-decoration:overline">B</span>，<span style="text-decoration:overline">(A+B)</span>=<span style="text-decoration:overline">A</span>·<span style="text-decoration:overline">B</span>'),
        # Complement law
        ('互补律：A·~A=0，A+~A=1',
         '互补律：A·<span style="text-decoration:overline">A</span>=0，A+<span style="text-decoration:overline">A</span>=1'),
        # Absorption/union methods
        ('A+~A=1', 'A+<span style="text-decoration:overline">A</span>=1'),
        ('A+~AB=A+B', 'A+<span style="text-decoration:overline">A</span>B=A+B'),
        ('利用A+~A=1', '利用A+<span style="text-decoration:overline">A</span>=1'),
        ('利用A+~AB', '利用A+<span style="text-decoration:overline">A</span>B'),
    ],
    'ch05.html': [
        ('J·~Q<sup>n</sup> + ~K·Q<sup>n</sup>',
         'J·<span style="text-decoration:overline">Q</span><sup>n</sup> + <span style="text-decoration:overline">K</span>·Q<sup>n</sup>'),
        ('S + ~R·Q<sup>n</sup>',
         'S + <span style="text-decoration:overline">R</span>·Q<sup>n</sup>'),
    ],
}

for fname, replacements in fixes.items():
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = 0
    for old, new in replacements:
        c = content.count(old)
        if c > 0:
            content = content.replace(old, new)
            changed += c

    if changed > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("%s: %d replacements" % (fname, changed))

# Fix generate_chapters.py source
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    content = f.read()

gen_fixes = {
    'J·~Q<sup>n</sup> + ~K·Q<sup>n</sup>': 'J·<span style="text-decoration:overline">Q</span><sup>n</sup> + <span style="text-decoration:overline">K</span>·Q<sup>n</sup>',
    'S + ~R·Q<sup>n</sup>': 'S + <span style="text-decoration:overline">R</span>·Q<sup>n</sup>',
    'A·~A=0': 'A·<span style="text-decoration:overline">A</span>=0',
    'A+~A=1': 'A+<span style="text-decoration:overline">A</span>=1',
    '摩根定律：~(A·B)=~A+~B，~(A+B)=~A·~B': '摩根定律：<span style="text-decoration:overline">(A·B)</span>=<span style="text-decoration:overline">A</span>+<span style="text-decoration:overline">B</span>，<span style="text-decoration:overline">(A+B)</span>=<span style="text-decoration:overline">A</span>·<span style="text-decoration:overline">B</span>',
    '互补律：A·~A=0，A+~A=1': '互补律：A·<span style="text-decoration:overline">A</span>=0，A+<span style="text-decoration:overline">A</span>=1',
    '利用A+~A=1': '利用A+<span style="text-decoration:overline">A</span>=1',
    '利用A+~AB': '利用A+<span style="text-decoration:overline">A</span>B',
    'A+~AB=A+B': 'A+<span style="text-decoration:overline">A</span>B=A+B',
}

changed = 0
for old, new in gen_fixes.items():
    c = content.count(old)
    if c > 0:
        content = content.replace(old, new)
        changed += c

if changed > 0:
    with open(gen_py, 'w', encoding='utf-8') as f:
        f.write(content)
    print("generate_chapters.py: %d replacements" % changed)
