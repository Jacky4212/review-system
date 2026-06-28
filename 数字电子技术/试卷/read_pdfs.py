#!/usr/bin/env python3
"""Extract text from all exam PDFs."""
import fitz
import os

base = os.path.dirname(os.path.abspath(__file__))
files = [f for f in os.listdir(base) if f.endswith('.pdf')]
files.sort()

for fname in files:
    path = os.path.join(base, fname)
    doc = fitz.open(path)
    out_name = fname.replace('.pdf', '_text.txt')
    out_path = os.path.join(base, out_name)

    print("处理: %s (%d页)" % (fname, len(doc)))

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("来源: %s\n总页数: %d\n\n" % (fname, len(doc)))
        for i in range(len(doc)):
            text = doc[i].get_text()
            f.write("=== 第%d页 ===\n" % (i+1))
            f.write(text)
            f.write("\n\n")

    doc.close()
    size = os.path.getsize(out_path)
    print("  已保存: %s (%d bytes)" % (out_name, size))
