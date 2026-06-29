#!/usr/bin/env python3
import olefile, glob, re, os

def extract_ppt_text(filepath):
    try:
        ole = olefile.OleFileIO(filepath)
        text_parts = []
        streams = ole.listdir()
        for stream_path in streams:
            try:
                data = ole.openstream(stream_path).read()
                # Try UTF-16LE
                decoded = data.decode('utf-16-le', errors='ignore')
                segments = re.findall(r'[一-鿿\w\s]{10,}', decoded)
                text_parts.extend(segments)
            except:
                pass
        ole.close()
        return '\n'.join(text_parts)
    except Exception as e:
        return f""

files = sorted(glob.glob('放射化学/*.ppt'))
files = [f for f in files if not os.path.basename(f).startswith('~')]

found = False
for f in files:
    text = extract_ppt_text(f)
    if '分支' in text:
        found = True
        print(f"\n{'='*60}")
        print(f"FILE: {f}")
        print('='*60)
        for line in text.split('\n'):
            if '分支' in line:
                idx = line.index('分支')
                start = max(0, idx-80)
                end = min(len(line), idx+150)
                print(f"...{line[start:end]}...")

# Also search for exact term 分支比
print("\n\n=== SEARCH FOR 分支比 ===")
for f in files:
    text = extract_ppt_text(f)
    if '分支比' in text:
        print(f"FOUND in: {f}")
        for line in text.split('\n'):
            if '分支比' in line:
                idx = line.index('分支比')
                start = max(0, idx-80)
                end = min(len(line), idx+150)
                print(f"  ...{line[start:end]}...")

if not found:
    print("NOT FOUND: 分支 in any radiochemistry PPT")

# Also check accelerator PPTs
print("\n\n=== CHECK ACCELERATOR PPTS ===")
acc_files = sorted(glob.glob('加速器/*.ppt'))
for f in acc_files:
    text = extract_ppt_text(f)
    if '分支' in text:
        print(f"\nFOUND in: {f}")
        for line in text.split('\n'):
            if '分支' in line:
                idx = line.index('分支')
                start = max(0, idx-60)
                end = min(len(line), idx+100)
                print(f"  ...{line[start:end]}...")
