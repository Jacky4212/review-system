"""
将PPT幻灯片导出为PNG图片（使用PowerPoint COM）
"""

import os, sys
import pythoncom
import win32com.client
from pptx import Presentation

PPT_DIR = r"D:\code\cherry studio\复习\放射化学"
SLIDE_DIR = r"D:\code\cherry studio\复习\slides"

def export_slides():
    os.makedirs(SLIDE_DIR, exist_ok=True)

    pythoncom.CoInitialize()
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    # ppt_app.Visible = 0  # Hidden

    total_exported = 0
    for fname in sorted(os.listdir(PPT_DIR)):
        if not fname.endswith('.ppt') or fname.startswith('~$'):
            continue
        ppt_path = os.path.join(PPT_DIR, fname)
        base = os.path.splitext(fname)[0]

        print(f"  Processing: {fname}")
        try:
            pres = ppt_app.Presentations.Open(ppt_path)
            slide_count = pres.Slides.Count
            for i in range(1, slide_count + 1):
                img_name = f"{base}_slide{i:03d}.png"
                img_path = os.path.join(SLIDE_DIR, img_name)
                if os.path.exists(img_path):
                    continue
                # Export as PNG (1920x1440 for standard slide)
                pres.Slides(i).Export(img_path, "png", 1920, 1440)
                total_exported += 1
            pres.Close()
            print(f"    Exported {slide_count} slides")
        except Exception as e:
            print(f"    ERROR: {e}")

    ppt_app.Quit()
    pythoncom.CoUninitialize()
    print(f"\nTotal exported: {total_exported} images to {SLIDE_DIR}")

if __name__ == "__main__":
    export_slides()
