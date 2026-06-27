#!/usr/bin/env python3
"""Fix NOT symbol ¬ → ~ in all HTML files and check for remaining PUA chars."""
import os

base = "D:/code/cherry studio/复习/数字电子技术"
files = [f'ch{i:02d}.html' for i in range(1, 11)] + ['chips.html']

for fname in files:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    # Fix NOT symbol: ¬ → ~ (tilde is clearer in Chinese textbook context)
    count_not = content.count('\xAC')
    if count_not > 0:
        content = content.replace('\xAC', '~')
        changes.append('NOT: %d' % count_not)

    # Check for any remaining PUA chars
    pua_set = set()
    for ch in content:
        cp = ord(ch)
        if 0xE000 <= cp <= 0xF8FF:
            pua_set.add('U+%04X' % cp)
    if pua_set:
        changes.append('PUA left: ' + ','.join(pua_set))

    if changes:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("%s: %s" % (fname, '; '.join(changes)))
    else:
        print("%s: clean" % fname)
