#!/usr/bin/env python3
"""Update generate_chapters.py with proper logic symbols."""
path = 'D:/code/cherry studio/复习/数字电子技术/generate_chapters.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old = '<li><strong>与运算</strong>（L = A \xb7 B）：只有当决定某一事件的条件全部具备时，这一事件才会发生。</li>\n      <li><strong>或运算</strong>（L = A + B）：只要有一个或几个条件具备时，事件就会发生。</li>\n      <li><strong>非运算</strong>（L = <span style="text-decoration:overline">A</span>）：条件具备时事件不发生，条件不具备时事件发生。</li>\n      <li><strong>与非</strong>：先与后非；<strong>或非</strong>：先或后非</li>\n      <li><strong>异或</strong>：两个输入变量的值相异，输出为1，否则为0。</li>\n      <li><strong>同或</strong>：两个输入变量的值相同，输出为1，否则为0。</li>'

new = '<li><strong>与运算</strong>（L = A \xb7 B = AB）：只有当决定某一事件的条件全部具备时，这一事件才会发生。</li>\n      <li><strong>或运算</strong>（L = A + B）：只要有一个或几个条件具备时，事件就会发生。</li>\n      <li><strong>非运算</strong>（L = <span style="text-decoration:overline">A</span>）：条件具备时事件不发生，条件不具备时事件发生。</li>\n      <li><strong>与非运算</strong>（L = <span style="text-decoration:overline">A\xb7B</span>）：先与后非，输入全1时输出0。</li>\n      <li><strong>或非运算</strong>（L = <span style="text-decoration:overline">A+B</span>）：先或后非，输入全0时输出1。</li>\n      <li><strong>异或运算</strong>（L = A ⊕ B）：两个输入变量的值相异，输出为1，否则为0。</li>\n      <li><strong>同或运算</strong>（L = A ⊙ B = <span style="text-decoration:overline">A⊕B</span>）：两个输入变量的值相同，输出为1，否则为0。</li>'

if old in c:
    c = c.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('not found')
    # Try simpler match
    if '异或' in c and '同或' in c:
        print('Content exists, but pattern mismatch')
