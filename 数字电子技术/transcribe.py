#!/usr/bin/env python3
"""Transcribe audio using local faster-whisper model."""
import os
import sys

from faster_whisper import WhisperModel

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whisper-tiny-model")
print("使用本地模型: " + model_path)

model = WhisperModel(model_path, device="cpu", compute_type="int8", local_files_only=True)

file = "185 7349 5867_20260622123532.m4a"
print("正在转写: " + file)
segments, info = model.transcribe(file, language="zh", beam_size=5)

print("\n检测到语言: " + info.language)
print("=" * 60)
results = []
for seg in segments:
    line = "[%0.1fs -> %0.1fs] %s" % (seg.start, seg.end, seg.text)
    print(line)
    results.append(seg.text)

full = " ".join(results)
print("\n\n=== 全文 ===")
print(full)

outfile = file.replace('.m4a', '.txt')
with open(outfile, 'w', encoding='utf-8') as f:
    f.write(full)
print("\n已保存到: " + outfile)
