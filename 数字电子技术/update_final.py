#!/usr/bin/env python3
"""Final update to logic ops section."""
path = 'D:/code/cherry studio/复习/数字电子技术/ch01.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 与非 line
c = c.replace(
    '<li><strong>与非运算</strong>（L = <span style="text-decoration:overline">A\xb7B</span> = <span style="text-decoration:overline">A</span>+<span style="text-decoration:overline">B</span>）：先与后非，输入全1时输出0。与-或表达式转换可用摩根定律。</li>',
    '<li><strong>与非运算</strong>（L = <span style="text-decoration:overline">A\xb7B</span> = <span style="text-decoration:overline">A</span>+<span style="text-decoration:overline">B</span> = <span style="text-decoration:overline">A</span>\xb7<span style="text-decoration:overline">B</span> + <span style="text-decoration:overline">A</span>\xb7B + A\xb7<span style="text-decoration:overline">B</span>）：先与后非，输入全1时输出0。</li>'
)

# Fix 或非 line - remove "与-或表达式转换可用摩根定律"
c = c.replace(
    '<li><strong>或非运算</strong>（L = <span style="text-decoration:overline">A+B</span> = <span style="text-decoration:overline">A</span>\xb7<span style="text-decoration:overline">B</span>）：先或后非，输入全0时输出1。与-或表达式转换可用摩根定律。</li>',
    '<li><strong>或非运算</strong>（L = <span style="text-decoration:overline">A+B</span> = <span style="text-decoration:overline">A</span>\xb7<span style="text-decoration:overline">B</span>）：先或后非，输入全0时输出1。</li>'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
