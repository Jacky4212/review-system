#!/usr/bin/env python3
"""Fix remaining navigation issues."""
import os

base = "D:/code/cherry studio/复习/数字电子技术"

# Fix ch01 — remove duplicate home link in bottom nav
ch01_path = os.path.join(base, 'ch01.html')
with open(ch01_path, 'r', encoding='utf-8') as f:
    c = f.read()

old = '<a href="index.html">← 返回首页</a>\n    <a href="index.html">课程首页</a>'
new = '<a href="index.html">← 返回首页</a>'
if old in c:
    c = c.replace(old, new)
    # Also fix topbar link
    c = c.replace('class="topbar-inner">\n    <a href="index.html">← 返回首页</a>',
                  'class="topbar-inner">\n    <a href="index.html">← 首页</a>')
    with open(ch01_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("ch01: fixed")
else:
    print("ch01: pattern not found")

# Fix chips — reorder bottom nav to have home first
chips_path = os.path.join(base, 'chips.html')
with open(chips_path, 'r', encoding='utf-8') as f:
    c = f.read()

old = '  <div class="nav-links">\n    <a href="ch10.html">← 第10章 模数与数模转换器</a>\n    <a href="index.html">← 返回首页</a>\n  </div>'
new = '  <div class="nav-links">\n    <a href="index.html">← 返回首页</a>\n    <a href="ch10.html">← 第10章 模数与数模转换器</a>\n  </div>'
if old in c:
    c = c.replace(old, new)
    with open(chips_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("chips: fixed")
else:
    print("chips: pattern not found, checking...")
    # Debug
    import re
    m = re.search(r'<div class="nav-links">.*?</div>', c, re.DOTALL)
    if m:
        print(f"  Found: {m.group()[:100]}")

# Fix topbar for auto-generated pages (ch04, etc.)
# ch04 topbar has "← 第3章" not "← 第3章 逻辑门电路" — this is intentional (short)
# But let me check if chips topbar is correct
with open(chips_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Check chips topbar has proper links
old = 'topbar-inner">\n    <a href="ch10.html">← 第10章</a>\n    <h2>常用芯片专题</h2>\n    <a href="index.html">首页 →</a>'
if old in c:
    print("chips topbar: OK")
else:
    print("chips topbar: checking...")

# Fix generate_chapters.py template for ch01
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    c = f.read()

old_src = "'prev': 'index.html', 'prev_label': '课程首页',"
new_src = "'prev': 'index.html', 'prev_label': '返回首页',"
if old_src in c:
    c = c.replace(old_src, new_src)
    # Also fix corresponding topbar label
    c = c.replace("'tprev': 'index.html', 'tprev_label': '← 返回首页',",
                  "'tprev': 'index.html', 'tprev_label': '← 首页',")
    with open(gen_py, 'w', encoding='utf-8') as f:
        f.write(c)
    print("generate_chapters.py: fixed ch01 labels")

# Regenerate
os.system(f'cd "{base}" && python generate_chapters.py')
print("Regenerated")
