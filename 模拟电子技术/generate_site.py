#!/usr/bin/env python3
"""Generate analog electronics review website v3 - following updated workflow."""
import json, re

with open('_ppt_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

CHAPTER_INFO = {
    'ch01.pptx': {'num': '1', 'title': '绪论', 'desc': '信号与频谱 · 放大电路模型 · 性能指标', 'tags': ['基础知识'], 'color': '#2d7fc1'},
    'ch02.pptx': {'num': '2', 'title': '运算放大器', 'desc': '理想运放 · 虚短虚断 · 同相/反相放大 · 积分微分', 'tags': ['核心器件'], 'color': '#27ae60'},
    'ch03.pptx': {'num': '3', 'title': '二极管及其基本电路', 'desc': 'PN结 · 二极管模型 · 整流·限幅·钳位 · 齐纳二极管', 'tags': ['基础器件'], 'color': '#e67e22'},
    'ch04  MOS管.pptx': {'num': '4', 'title': 'MOS场效应管及其放大电路', 'desc': '增强型/耗尽型 · 共源/共漏/共栅 · 小信号模型', 'tags': ['核心器件', '放大电路'], 'color': '#8e44ad'},
    'ch05  BJT管.pptx': {'num': '5', 'title': '双极结型三极管(BJT)及其放大电路', 'desc': 'NPN/PNP · 共射/共集/共基 · H参数模型', 'tags': ['核心器件', '放大电路'], 'color': '#c0392b'},
    'ch07.pptx': {'num': '7', 'title': '模拟集成电路', 'desc': '电流源 · 差分放大 · 有源负载 · CMOS运放 · 运放参数', 'tags': ['集成电路'], 'color': '#16a085'},
    'ch08.pptx': {'num': '8', 'title': '反馈放大电路', 'desc': '反馈分类 · 四种组态 · 深度负反馈 · 自激振荡与补偿', 'tags': ['核心概念'], 'color': '#2980b9'},
    'ch09.pptx': {'num': '9', 'title': '功率放大电路', 'desc': '甲类·乙类·甲乙类·丁类 · OCL/OTL · 互补对称 · 交越失真', 'tags': ['应用'], 'color': '#d35400'},
}

CHAPTER_ORDER = ['ch01.pptx', 'ch02.pptx', 'ch03.pptx', 'ch04  MOS管.pptx',
                 'ch05  BJT管.pptx', 'ch07.pptx', 'ch08.pptx', 'ch09.pptx']

CHAPTER_SHORT = {
    'ch01.pptx': 'ch01', 'ch02.pptx': 'ch02', 'ch03.pptx': 'ch03',
    'ch04  MOS管.pptx': 'ch04', 'ch05  BJT管.pptx': 'ch05',
    'ch07.pptx': 'ch07', 'ch08.pptx': 'ch08', 'ch09.pptx': 'ch09'
}

# ===== Text processing helpers =====

PUA_MAP = {
    # PPT private-use-area symbols → readable alternatives
    0xF02D: '◆', 0xF044: '●', 0xF057: '✓', 0xF05E: '▲',
    0xF061: '▶', 0xF062: '▼', 0xF068: '▲', 0xF06A: '◆',
    0xF06C: '●', 0xF06D: '★', 0xF070: '□', 0xF074: '▪',
    0xF077: '◇', 0xF07E: '▪', 0xF0A2: '▶', 0xF0A3: '◀',
    0xF0AB: '↑', 0xF0AD: '→', 0xF0AE: '↓', 0xF0AF: '↕',
    0xF0B0: '↔', 0xF0B1: '↵', 0xF0B3: '↗', 0xF0B7: '◆',
    0xF0B9: '●', 0xF0BB: '▲', 0xF0BD: '▼', 0xF0D6: '✓',
    0xF0D7: '✗',
}

GREEK_MAP = {
    0x00B5: 'μ', 0x0394: 'Δ', 0x03A9: 'Ω', 0x03BC: 'μ',
    0x03C0: 'π', 0x03C9: 'ω',
}

def fmt_text(text):
    """Apply subscript/superscript formatting and escape HTML."""
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('−', '−').replace('×', '×').replace('≈', '≈').replace('≥', '≥').replace('≤', '≤')
    text = text.replace('→', '→').replace('±', '±').replace('·', '·')
    text = text.replace('–', '–').replace('—', '—')
    text = text.replace('"', '&ldquo;').replace('"', '&rdquo;')
    text = text.replace('•', '·')

    # Replace PUA characters
    chars = list(text)
    for i, c in enumerate(chars):
        code = ord(c)
        if code in PUA_MAP:
            chars[i] = PUA_MAP[code]
        elif code in GREEK_MAP:
            chars[i] = GREEK_MAP[code]
    text = ''.join(chars)

    # Process subscript patterns:
    # VGS, VDS, VGSQ, VTN, VTP, VBE, VCE, VCC, VDD, VSS, VGG, IDQ, IC, IB, IE, iD, iC, iB, vGS, vDS, vBE, vCE
    # Pattern: optional lowercase prefix + capital letter(s) + capital/number suffix
    sub_terms = [
        (r'V(\s*)([A-Z]+[0-9]*)', r'V\1<sub>\2</sub>'),
        (r'I(\s*)([A-Z]+[0-9]*)', r'I\1<sub>\2</sub>'),
        (r'i(\s*)([A-Z]+[0-9]*)', r'i\1<sub>\2</sub>'),
        (r'v(\s*)([A-Z]+[0-9]*)', r'v\1<sub>\2</sub>'),
        (r'P(\s*)([A-Z]+)', r'P\1<sub>\2</sub>'),
        (r'R(\s*)([A-Z0-9]+)', r'R\1<sub>\2</sub>'),
        (r'r(\s*)([a-z0-9]+)', r'r\1<sub>\2</sub>'),
        (r'g(\s*)(m)', r'g\1<sub>\2</sub>'),
        (r'A(\s*)(vo|vf|i|v|r|g)', r'A\1<sub>\2</sub>'),
        (r'K(\s*)(CMR|n)', r'K\1<sub>\2</sub>'),
        (r'B(\s*)(WG)', r'B\1<sub>\2</sub>'),
        (r'V(\s*)(BR)', r'V\1<sub>\2</sub>'),
    ]
    for pattern, replacement in sub_terms:
        text = re.sub(pattern, replacement, text)

    # Degree symbol
    text = text.replace('°', '°')

    return text


def is_heading(text):
    """Check if text looks like a heading (short, no period end)."""
    if len(text) > 60:
        return False
    end_chars = text[-1] if text else ''
    if end_chars in '。；，？！)]':
        return False
    if text.startswith('图') or text.startswith('表'):
        return False
    if any(c in text for c in '＝≈≥≤'):
        return False
    return True


def is_formula(text):
    """Check if text contains mathematical formula patterns."""
    if any(c in text for c in ('＝', '≈', '≥', '≤', '∫', '∑', '∂', 'π')):
        return True
    if re.search(r'[A-Za-z]\s*[＝≈≥≤]', text):
        return True
    return False


def fmt_text_paragraph(text):
    """Format a text paragraph with proper HTML."""
    text_f = fmt_text(text)
    if is_formula(text):
        return '      <div class="formula">%s</div>' % text_f
    elif is_heading(text):
        return '      <h3>%s</h3>' % text_f
    else:
        return '      <p>%s</p>' % text_f


def fmt_table(rows):
    """Format table data as HTML table."""
    if not rows:
        return ''
    ncols = max(len(r) for r in rows)
    html = '      <table>\n'
    for ri, row in enumerate(rows):
        padded = row + [''] * (ncols - len(row))
        tag = 'th' if ri == 0 else 'td'
        cells = ''.join('        <%s>%s</%s>\n' % (tag, fmt_text(c), tag) for c in padded)
        html += '      <tr>\n%s      </tr>\n' % cells
    html += '      </table>'
    return html


# ===== CSS template (used by both index and chapter) =====
INDEX_CSS = '''
  :root {
    --primary: #1a3a5c;
    --accent: #2d7fc1;
    --bg: #f5f7fa;
    --card-bg: #ffffff;
    --text: #2c3e50;
    --text-light: #7f8c8d;
    --border: #e1e8ed;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }
  .header {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: #fff;
    padding: 40px 20px;
    text-align: center;
  }
  .header h1 { font-size: 2.2em; margin-bottom: 8px; }
  .header p { opacity: 0.9; font-size: 1.1em; }
  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }
  .info-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .info-card h2 {
    font-size: 1.4em;
    color: var(--primary);
    border-left: 4px solid var(--accent);
    padding-left: 14px;
    margin-bottom: 16px;
  }
  .info-card p { color: var(--text-light); margin-bottom: 8px; }
  .chapter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    margin-top: 20px;
  }
  .chapter-card {
    background: var(--card-bg);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-left: 4px solid var(--accent);
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
    text-decoration: none;
    display: block;
    color: var(--text);
  }
  .chapter-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  }
  .chapter-card .num {
    font-size: 0.85em;
    color: var(--accent);
    font-weight: 600;
  }
  .chapter-card h3 { font-size: 1.15em; margin: 4px 0 8px; }
  .chapter-card .desc {
    font-size: 0.9em;
    color: var(--text-light);
    line-height: 1.5;
  }
  .chapter-card .tag {
    display: inline-block;
    font-size: 0.78em;
    padding: 2px 10px;
    border-radius: 12px;
    margin-right: 4px;
  }
  .footer {
    text-align: center;
    padding: 30px;
    color: var(--text-light);
    font-size: 0.85em;
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }
  .footer a { color: var(--accent); text-decoration: none; }
  @media (max-width: 640px) {
    .header h1 { font-size: 1.6em; }
    .chapter-grid { grid-template-columns: 1fr; }
  }
'''

CHAPTER_CSS = '''
  :root {
    --primary: #1a3a5c;
    --accent: %s;
    --bg: #f5f7fa;
    --card-bg: #ffffff;
    --text: #2c3e50;
    --text-light: #7f8c8d;
    --border: #e1e8ed;
    --code-bg: #f0f4f8;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
  }
  .topbar {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: #fff;
    padding: 20px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }
  .topbar-inner {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }
  .topbar a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.9em; }
  .topbar a:hover { color: #fff; }
  .topbar h2 { font-size: 1.2em; }
  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }
  .section {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .section-num {
    font-size: 0.8rem;
    color: var(--text-light);
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
  }
  .section h3 {
    font-size: 1.1em;
    color: var(--accent);
    margin: 18px 0 8px;
    padding-bottom: 4px;
    border-bottom: 1px dashed var(--border);
  }
  .section h3:first-of-type { margin-top: 0; }
  .section p { margin-bottom: 8px; color: var(--text); font-size: 0.95em; }
  .section p:last-child { margin-bottom: 0; }
  .highlight {
    background: #fffbe6;
    border-left: 3px solid #f0c040;
    padding: 12px 16px;
    margin: 12px 0;
    border-radius: 6px;
    font-size: 0.95em;
  }
  .def-box {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.95em;
  }
  .def-box strong { color: var(--accent); }
  .formula {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 10px 16px;
    margin: 10px 0;
    text-align: center;
    font-size: 1em;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
  table {
    width: 100%%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 0.95em;
  }
  th, td {
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: center;
  }
  th {
    background: var(--code-bg);
    font-weight: 600;
    color: var(--primary);
  }
  .nav-links { margin-top: 30px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
  .nav-links a {
    display: inline-block;
    padding: 10px 24px;
    background: var(--card-bg);
    border-radius: 8px;
    text-decoration: none;
    color: var(--accent);
    border: 1px solid var(--border);
    transition: all 0.2s;
    font-size: 0.95em;
  }
  .nav-links a:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
  .nav-links span { flex: 1; }
  .footer { text-align: center; padding: 24px; color: var(--text-light); font-size: 0.85em; border-top: 1px solid var(--border); }
  @media (max-width: 640px) {
    .section { padding: 16px; }
    .topbar h2 { font-size: 1em; }
    table { font-size: 0.85em; }
    th, td { padding: 6px 8px; }
  }
'''


# ===== Index page =====
def gen_index():
    cards = []
    for fname in CHAPTER_ORDER:
        info = CHAPTER_INFO[fname]
        fshort = CHAPTER_SHORT[fname]
        tags = ''.join('<span class="tag" style="background:#e8f4fd;color:%s;">%s</span>' % (info['color'], t) for t in info['tags'])
        card = '''
      <a href="%s.html" class="chapter-card" style="border-left-color:%s;">
        <div class="num">第%s章</div>
        <h3>%s</h3>
        <div class="desc">%s</div>
        <div style="margin-top:10px;">%s</div>
      </a>''' % (fshort, info['color'], info['num'], info['title'], info['desc'], tags)
        cards.append(card)

    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>模拟电子技术 - 复习系统</title>
<style>%s</style>
</head>
<body>
<div class="header">
  <h1>&#x1F4D8; 模拟电子技术</h1>
  <p>Analog Electronics &middot; 课程复习笔记</p>
</div>
<div class="container">
  <div class="info-card">
    <h2>课程说明</h2>
    <p>本复习网站基于课程 PPT 内容整理，涵盖模拟电子技术的核心知识点。</p>
    <p>内容均来源于 PPT 原话，适合考前复习与知识梳理。</p>
  </div>
  <div class="info-card">
    <h2>&#x1F4C2; 章节导航</h2>
    <div class="chapter-grid">%s
    </div>
  </div>
</div>
<div class="footer">
  <p>内容来源: 模拟电子技术课程PPT</p>
  <p><a href="https://github.com/Jacky4212/review-system.git">GitHub: Jacky4212/review-system</a></p>
</div>
</body>
</html>''' % (INDEX_CSS, '\n'.join(cards))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Generated: index.html')


# ===== Chapter pages =====
def gen_chapter(fname, info, slides):
    color = info['color']
    fshort = CHAPTER_SHORT[fname]
    idx = CHAPTER_ORDER.index(fname)
    prev_ch = CHAPTER_ORDER[idx-1] if idx > 0 else None
    next_ch = CHAPTER_ORDER[idx+1] if idx < len(CHAPTER_ORDER)-1 else None

    # Navigation
    nav_items = ['<a href="index.html">&larr; 返回首页</a>']
    if prev_ch:
        pshort = CHAPTER_SHORT[prev_ch]
        pt = CHAPTER_INFO[prev_ch]['title']
        pn = CHAPTER_INFO[prev_ch]['num']
        nav_items.append('<a href="%s.html">&larr; 第%s章 %s</a>' % (pshort, pn, pt))
    else:
        nav_items.append('<span></span>')
    if next_ch:
        nshort = CHAPTER_SHORT[next_ch]
        nt = CHAPTER_INFO[next_ch]['title']
        nn = CHAPTER_INFO[next_ch]['num']
        nav_items.append('<a href="%s.html">第%s章 %s &rarr;</a>' % (nshort, nn, nt))
    nav_html = '\n    '.join(nav_items)

    # Topbar next link
    if next_ch:
        nshort = CHAPTER_SHORT[next_ch]
        nt = CHAPTER_INFO[next_ch]['title']
        nn = CHAPTER_INFO[next_ch]['num']
        topbar_next = '第%s章 %s &rarr;' % (nn, nt)
        topbar_next_href = '%s.html' % nshort
    else:
        topbar_next = '返回首页'
        topbar_next_href = 'index.html'

    # Build content sections
    sections = []
    for s in slides:
        parts = []
        for item in s['items']:
            if item['type'] == 'table':
                parts.append(fmt_table(item['rows']))
            else:
                text = item['text']
                if not text.strip():
                    continue
                parts.append(fmt_text_paragraph(text))
        if parts:
            block = '''
    <div class="section">
      <div class="section-num">第 %d 页</div>
%s
    </div>''' % (s['slide'], '\n'.join(parts))
            sections.append(block)

    content_str = '\n'.join(sections)
    css = CHAPTER_CSS % color

    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第%s章 %s - 模拟电子技术</title>
<style>%s</style>
</head>
<body>
<div class="topbar">
  <div class="topbar-inner">
    <a href="index.html">&larr; 返回首页</a>
    <h2>第%s章 %s</h2>
    <a href="%s">%s</a>
  </div>
</div>
<div class="container">%s
  <div class="nav-links">
    %s
  </div>
</div>
<div class="footer">
  <p>内容来源: 模拟电子技术课程PPT &middot; 第%s章 %s</p>
</div>
</body>
</html>''' % (info['num'], info['title'], css,
              info['num'], info['title'],
              topbar_next_href, topbar_next,
              content_str, nav_html,
              info['num'], info['title'])

    out_name = '%s.html' % fshort
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Generated: %s' % out_name)


# ===== Main =====
if __name__ == '__main__':
    gen_index()
    for fname in CHAPTER_ORDER:
        info = CHAPTER_INFO[fname]
        slides = data.get(fname, [])
        gen_chapter(fname, info, slides)
    print('All done!')
