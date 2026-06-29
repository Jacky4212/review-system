#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import olefile, glob, re, os

KEYWORD = '分支'  # 分支
KEYWORD2 = '分支比'  # 分支比

def extract_ppt_text(filepath):
    try:
        with olefile.OleFileIO(filepath) as ole:
            text_parts = []
            for stream_path in ole.listdir():
                data = ole.openstream(stream_path).read()
                decoded = data.decode('utf-16-le', errors='ignore')
                segments = re.findall(r'[一-鿿\w\s]{10,}', decoded)
                text_parts.extend(segments)
            return '\n'.join(text_parts)
    except Exception as e:
        return f""

files = sorted(glob.glob('放射化学/*.ppt'))
files = [f for f in files if not os.path.basename(f).startswith('~')]

found_any = False
for f in files:
    text = extract_ppt_text(f)
    if KEYWORD in text:
        found_any = True
        print(f"\n{'='*60}")
        print(f"FILE: {f}")
        print('='*60)
        for line in text.split('\n'):
            if KEYWORD in line:
                idx = line.index(KEYWORD)
                start = max(0, idx-80)
                end = min(len(line), idx+150)
                print(f"  ...{line[start:end]}...")

if not found_any:
    print("在放射化学PPT中未找到" + KEYWORD)

# Also check accelerator
print(f"\n\n=== 搜索加速器PPT中的「{KEYWORD}」===")
acc_files = sorted(glob.glob('加速器/*.ppt'))
acc_found = False
for f in acc_files:
    text = extract_ppt_text(f)
    if KEYWORD in text:
        acc_found = True
        print(f"\nFOUND in: {f}")
        for line in text.split('\n'):
            if KEYWORD in line:
                idx = line.index(KEYWORD)
                start = max(0, idx-60)
                end = min(len(line), idx+100)
                print(f"  ...{line[start:end]}...")

if not acc_found:
    print("在加速器PPT中未找到" + KEYWORD)
