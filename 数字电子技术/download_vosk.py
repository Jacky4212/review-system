#!/usr/bin/env python3
"""Download Vosk Chinese speech recognition model."""
import urllib.request
import zipfile
import os
import ssl
import sys

print("Python 版本: %s" % sys.version)

# Disable SSL verification entirely
ctx = ssl._create_unverified_context()

model_url = "https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip"
model_zip = "vosk-model-small-cn-0.22.zip"
model_dir = "vosk-model-small-cn-0.22"

if os.path.exists(model_dir):
    print("模型已存在")
else:
    print("正在下载中文语音模型（约42MB）...")
    print("从: " + model_url)

    try:
        req = urllib.request.Request(model_url)
        with urllib.request.urlopen(req, context=ctx, timeout=120) as response:
            print("连接成功! 文件大小: %s bytes" % response.headers.get('Content-Length', '未知'))
            total = 0
            with open(model_zip, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    total += len(chunk)
                    if total % 1048576 < 8192:
                        print("已下载: %d MB" % (total // 1048576))
        print("下载完成 (%d bytes)" % total)
    except Exception as e:
        print("下载出错: %s" % e)
        # Try alternative URL
        print("尝试备用地址...")
        sys.exit(1)

    print("正在解压...")
    with zipfile.ZipFile(model_zip, 'r') as zf:
        zf.extractall()
    os.remove(model_zip)
    print("模型解压完成！")
