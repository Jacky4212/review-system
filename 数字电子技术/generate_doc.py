#!/usr/bin/env python3
"""Generate a detailed step-by-step Word document of the entire process."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

doc = Document()

# --- Styles ---
style = doc.styles['Normal']
font = style.font
font.name = '微软雅黑'
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

# ===== Title =====
title = doc.add_heading('', level=0)
run = title.add_run('数字电子技术复习系统 — 完整搭建流程')
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x1a, 0x3a, 0x5c)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph('')  # spacing

# ===== Overview =====
h = doc.add_heading('一、任务概述', level=1)
p = doc.add_paragraph()
p.add_run('目标：').bold = True
p.add_run('基于课程PPT文件，搭建一个可直接访问的静态复习网站，包含重点章节的知识梳理和常用芯片专题。')
doc.add_paragraph('')

# ===== Step 1 =====
doc.add_heading('二、详细流程', level=1)

doc.add_heading('Step 1 — PPT文字内容提取', level=2)
p = doc.add_paragraph()
p.add_run('工具：').bold = True
p.add_run('python-pptx 库')
doc.add_paragraph('操作步骤：', style='List Bullet')
steps = [
    '编写 extract_pptx.py 脚本，遍历当前目录下所有 .pptx 文件',
    '对每个文件，逐页读取所有文本框（shape.has_text_frame）和表格（shape.has_table）中的文字',
    '将每页文字合并，写入 提取内容/ 目录下对应的 .txt 文件',
    '跳过文件名含 (2) 的重复文件，保留原文件',
]
for s in steps:
    doc.add_paragraph(s, style='List Number')
p = doc.add_paragraph()
p.add_run('关键代码片段：').bold = True
doc.add_paragraph('for shape in slide.shapes:\n    if shape.has_text_frame:\n        for para in shape.text_frame.paragraphs:\n            if para.text.strip(): slide_text.append(para.text)', style='No Spacing')

doc.add_heading('Step 2 — 录音转写', level=2)
p = doc.add_paragraph()
p.add_run('工具：').bold = True
p.add_run('faster-whisper（本地离线语音识别）')
doc.add_paragraph('操作步骤：', style='List Bullet')
steps2 = [
    '安装 faster-whisper：pip install faster-whisper',
    '由于网络SSL证书问题，使用 curl -k 直接从 HuggingFace 下载模型文件到本地 whisper-tiny-model/ 目录',
    '模型文件包括：config.json, model.bin(~75MB), tokenizer.json, vocabulary.txt',
    '编写 transcribe.py，用本地模型对 .m4a 录音文件进行语音转写',
    '设置 language="zh"，得到中文转写结果，保存为 .txt 文件',
]
for s in steps2:
    doc.add_paragraph(s, style='List Number')
p = doc.add_paragraph()
p.add_run('注：').bold = True
p.add_run('如果网络环境不允许从 HuggingFace 下载，可用 curl -k 绕过SSL验证。')

doc.add_heading('Step 3 — 静态网站搭建', level=2)
p = doc.add_paragraph()
p.add_run('工具：').bold = True
p.add_run('纯 HTML + CSS，无任何外部依赖')
doc.add_paragraph('网站结构：', style='List Bullet')
doc.add_paragraph('数字电子技术/', style='List Number')
doc.add_paragraph('  ├── index.html      ← 课程首页（章节导航卡片）', style='List Number')
doc.add_paragraph('  ├── ch03.html       ← 第3章 逻辑门电路', style='List Number')
doc.add_paragraph('  ├── ch07.html       ← 第7章 半导体存储器', style='List Number')
doc.add_paragraph('  ├── ch10.html       ← 第10章 模数与数模转换器', style='List Number')
doc.add_paragraph('  └── chips.html      ← 常用芯片专题(555/161/138)', style='List Number')

doc.add_paragraph('')
p = doc.add_paragraph()
p.add_run('设计要点：').bold = True
doc.add_paragraph('内容全部基于 PPT 原话整理，标记来源页码', style='List Bullet')
doc.add_paragraph('每个芯片（555/161/138）都配有功能表（真值表）和典型应用公式', style='List Bullet')
doc.add_paragraph('响应式设计，兼容手机端', style='List Bullet')
doc.add_paragraph('章节间有上下页导航，方便浏览', style='List Bullet')

doc.add_heading('Step 4 — Git 提交与推送', level=2)
doc.add_paragraph('操作步骤：', style='List Bullet')
steps4 = [
    'cd 到上级目录（D:\\code\\cherry studio\\复习\\），这是 git 仓库根目录',
    'git add "数字电子技术/*.html" 添加新文件',
    'git commit -m "feat: 数字电子技术静态复习网站"',
    'git push origin master 推送到 GitHub',
]
for s in steps4:
    doc.add_paragraph(s, style='List Number')

doc.add_heading('Step 5 — 上级首页更新', level=2)
doc.add_paragraph('将根目录 index.html 从外部跳转页改为课程导航页，包含指向 数字电子技术 的卡片入口。')

doc.add_heading('Step 6 — 启用 GitHub Pages', level=2)
doc.add_paragraph('操作步骤：', style='List Bullet')
steps6 = [
    '使用 gh CLI：gh api repos/Jacky4212/review-system/pages --method POST --field source=\'{"branch":"master","path":"/"}\'',
    '等待 GitHub Pages 构建完成（状态变为 built）',
    '访问 https://jacky4212.github.io/review-system/ 即可看到上级首页',
    '点击 "数字电子技术基础" 卡片进入复习网站',
]
for s in steps6:
    doc.add_paragraph(s, style='List Number')

# ===== File Tree =====
doc.add_heading('三、最终文件结构', level=1)
doc.add_paragraph('D:\\code\\cherry studio\\复习\\（Git仓库根目录）')
tree = [
    '├── index.html              ← 上级首页（课程导航）',
    '├── 数字电子技术/',
    '│   ├── index.html          ← 课程首页（章节导航）',
    '│   ├── ch03.html           ← 第3章 逻辑门电路',
    '│   ├── ch07.html           ← 第7章 半导体存储器',
    '│   ├── ch10.html           ← 第10章 ADC/DAC',
    '│   ├── chips.html          ← 芯片专题(555/161/138)',
    '│   ├── 提取内容/           ← PPT文字提取结果',
    '│   └── 185 ... .txt        ← 录音转写结果',
    '├── 放射化学/',
    '├── 加速器/',
    '└── ...其他文件',
]
for t in tree:
    p = doc.add_paragraph(t)
    p.style.font.size = Pt(9)

# ===== Key formulas =====
doc.add_heading('四、关键公式速查', level=1)

doc.add_heading('555定时器', level=2)
formulas = [
    ('单稳态脉宽', 'tw ≈ 1.1 RC'),
    ('多谐振荡高电平时间', 'tpH ≈ 0.7 (R1 + R2) C'),
    ('多谐振荡低电平时间', 'tpL ≈ 0.7 R2 C'),
    ('多谐振荡周期', 'T ≈ 0.7 (R1 + 2R2) C'),
    ('施密特正向阈值', 'VT+ = 2/3 VCC'),
    ('施密特负向阈值', 'VT- = 1/3 VCC'),
]
for name, formula in formulas:
    p = doc.add_paragraph()
    p.add_run(f'{name}：').bold = True
    p.add_run(formula)

doc.add_heading('74LVC161计数器', level=2)
p = doc.add_paragraph()
p.add_run('并行进位输出：').bold = True
p.add_run('TC = CET · Q3Q2Q1Q0')

doc.add_heading('D/A转换器（倒T形电阻网络）', level=2)
p = doc.add_paragraph()
p.add_run('输出模拟电压：').bold = True
p.add_run('vO = – K · NB  (与输入二进制数成正比)')

doc.add_heading('A/D转换器', level=2)
p = doc.add_paragraph()
p.add_run('采样定理：').bold = True
p.add_run('fs ≥ 2fimax')

# ===== Reference =====
doc.add_heading('五、参考资料', level=1)
refs = [
    '华中科技大学《数字电子技术基础》课程PPT（全部10章）',
    'GitHub仓库: https://github.com/Jacky4212/review-system',
    '在线访问: https://jacky4212.github.io/review-system/',
    'faster-whisper: https://github.com/SYSTRAN/faster-whisper',
    'Vosk: https://alphacephei.com/vosk/',
]
for r in refs:
    doc.add_paragraph(r, style='List Bullet')

# ===== Footer =====
doc.add_paragraph('')
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('— 文档自动生成于 2026年6月 —').font.color.rgb = RGBColor(0x95, 0xa5, 0xa6)

# ===== Save =====
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '搭建流程文档.docx')
doc.save(out_path)
print("文档已生成: " + out_path)
