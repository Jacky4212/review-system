#!/usr/bin/env python3
"""Check HTML files for PPT extraction errors propagated to website."""
import os

base = "D:/code/cherry studio/复习/数字电子技术"
html_files = [f'ch{i:02d}.html' for i in range(1, 11)] + ['chips.html', 'index.html', 'methods.html']

# Check patterns in HTML files
checks = {
    '或相': 'PPT笔误，应为"或项"',
    '辑辑': 'PPT重复字，应为"逻辑"',
    '触法器': 'PPT笔误，应为"触发器"',
    '丛发': 'PPT用词，应确认是否为"突发"',
    '位线': 'PPT用词，存储领域用"位线"正确',
}

print("=== 检查HTML文件中的可疑词汇 ===")
for fname in html_files:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for pattern, note in checks.items():
        count = content.count(pattern)
        if count > 0:
            print(f"  {fname}: '{pattern}'出现{count}次 - {note}")

# Also check for known good patterns that might be missing
print("\n=== 检查内容完整性 ===")

# Check if methods.html covers expected topics
methods_path = os.path.join(base, 'methods.html')
if os.path.exists(methods_path):
    with open(methods_path, 'r', encoding='utf-8') as f:
        m = f.read()
    topics = ['数制转换', '真值表', '卡诺图', '最小项', '最大项', '对偶',
              '组合逻辑', '竞争冒险', '时序逻辑', '计数器', 'DAC', 'ADC',
              '采样定理', '量化']
    for t in topics:
        if t not in m:
            print(f"  methods.html 缺少: {t}")

print("\n=== 完成 ===")
