#!/usr/bin/env python3
"""Fix the syntax error in generate_all_answers.py."""
path = 'D:/code/cherry studio/复习/数字电子技术/试卷/generate_all_answers.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic 4-argument call with 3-argument call
old = """add_q(doc1,
    '12. （有时序电路状态图，见试卷）',
    '【此题含状态图，需根据状态转换图分析输出序列。】',
    '）'"""

new = """add_q(doc1,
    '12. （有时序电路状态图，见试卷）',
    '【此题含状态图，需根据状态转换图分析输出序列。】')"""

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("fixed: removed extra source param")
else:
    print("pattern not found, trying alternative...")
    # Try without the closing paren
    alt_old = """add_q(doc1,
    '12. （有时序电路状态图，见试卷）',
    '【此题含状态图，需根据状态转换图分析输出序列。】',
    '）"""
    if alt_old in content:
        content = content.replace(alt_old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("fixed with alt pattern")
    else:
        print("still not found")
