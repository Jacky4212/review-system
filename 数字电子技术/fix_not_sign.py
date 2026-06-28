#!/usr/bin/env python3
"""Fix ch01.html: remove NOT sign char from non operation."""
for path in [
    'D:/code/cherry studio/复习/数字电子技术/ch01.html',
    'D:/code/cherry studio/复习/数字电子技术/generate_chapters.py'
]:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    # Remove the problematic character
    old = ' = \xAC'
    if old in c:
        c = c.replace(old, '')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'Fixed: {path}')
    else:
        print(f'Not found in: {path}')
