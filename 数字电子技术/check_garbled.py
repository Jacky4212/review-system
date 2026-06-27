#!/usr/bin/env python3
"""Check extracted text for garbled characters."""
import os

extract_dir = "D:/code/cherry studio/复习/数字电子技术/提取内容"
files = sorted([f for f in os.listdir(extract_dir) if f.endswith('.txt')])

# Search for specific problematic patterns from PPT extraction
patterns = {
    '': '乘号x错误',
    '': '减号-错误',
    '': 'v字母错误',
    '': '箭头错误',
    '': '等号=错误',
    '': '加号+错误',
    '': '大于号>错误',
    '': '小于号<错误',
    '': '空格错误',
    '▪': '黑色方块',
}

print("=== 搜索各文件中的可疑字符 ===\n")
for fname in files:
    path = os.path.join(extract_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    found = set()
    for ch in content:
        cp = ord(ch)
        # Private Use Area (often garbled from PPT)
        if 0xE000 <= cp <= 0xF8FF:
            found.add('PUA-U+%04X' % cp)
        elif 0x0080 <= cp <= 0x00A0 and cp not in (0x0085, 0x00A0, 0x00A0):
            found.add('CTRL-U+%04X' % cp)

    if found:
        print("%s: %s" % (fname, ', '.join(sorted(found))))

# Also dump lines containing specific patterns
print("\n=== 包含特殊PUA字符的行 ===\n")
for fname in files:
    path = os.path.join(extract_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        for ch in line:
            if 0xE000 <= ord(ch) <= 0xF8FF:
                # Show context around the garbled character
                context = ''
                for c in line.strip():
                    if 0xE000 <= ord(c) <= 0xF8FF:
                        context += '[U+%04X]' % ord(c)
                    else:
                        context += c
                print("%s:%d: %s" % (fname, i, context[:120]))
                break
