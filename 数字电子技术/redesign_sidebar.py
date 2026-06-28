#!/usr/bin/env python3
"""Redesign sidebar with professional styling."""
import os, re

base = "D:/code/cherry studio/复习/数字电子技术"

# Professional sidebar CSS
sidebar_css = '''
  /* ===== Left Sidebar ===== */
  .sidebar {
    position: fixed; top: 0; left: 0; width: 210px; height: 100vh;
    background: #ffffff; border-right: 1px solid #edf2f7;
    z-index: 100; overflow-y: auto;
    display: flex; flex-direction: column;
  }
  .sidebar-header {
    padding: 22px 18px 16px;
    border-bottom: 1px solid #f1f5f9;
  }
  .sidebar-header .site-name {
    font-size: 1rem; font-weight: 700;
    color: #0f172a; letter-spacing: -0.01em;
  }
  .sidebar-header .site-sub {
    font-size: 0.7rem; color: #94a3b8;
    margin-top: 2px; font-weight: 400;
  }
  .sidebar-nav { flex: 1; padding: 10px 0 16px; }
  .sidebar-nav .group-label {
    font-size: 0.62rem; font-weight: 600; color: #94a3b8;
    padding: 14px 18px 4px; letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .sidebar-nav a {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 18px; margin: 1px 8px; border-radius: 6px;
    font-size: 0.8rem; color: #334155;
    text-decoration: none; transition: all 0.15s ease;
    border-left: 3px solid transparent;
  }
  .sidebar-nav a:hover {
    background: #f1f5f9; color: #0f172a;
    border-left-color: #cbd5e1;
  }
  .sidebar-nav a.current {
    background: #eff6ff; color: #2563eb;
    border-left-color: #2563eb; font-weight: 600;
  }
  .sidebar-nav a .tag {
    display: inline-flex; align-items: center; justify-content: center;
    width: 20px; height: 20px; border-radius: 4px;
    background: #f1f5f9; font-size: 0.65rem; font-weight: 600;
    color: #64748b; flex-shrink: 0;
  }
  .sidebar-nav a:hover .tag { background: #e2e8f0; }
  .sidebar-nav a.current .tag { background: #dbeafe; color: #2563eb; }

  /* Layout offsets */
  .container { margin-left: 210px; }
  .topbar { left: 210px; width: calc(100% - 210px); }
  .footer { margin-left: 210px; }

  @media (max-width: 768px) {
    .sidebar { display: none; }
    .container { margin-left: 0; }
    .topbar { left: 0; width: 100%; }
    .footer { margin-left: 0; }
  }
'''

sidebar_html = '''<nav class="sidebar">
  <div class="sidebar-header">
    <div class="site-name">数字电子技术</div>
    <div class="site-sub">基础 · 复习系统</div>
  </div>
  <div class="sidebar-nav">
    <div class="group-label">基础理论</div>
    <a href="ch01.html"><span class="tag">1</span>数字逻辑概论</a>
    <a href="ch02.html"><span class="tag">2</span>逻辑代数与HDL</a>
    <a href="ch03.html"><span class="tag">3</span>逻辑门电路</a>

    <div class="group-label">组合与时序</div>
    <a href="ch04.html"><span class="tag">4</span>组合逻辑电路</a>
    <a href="ch05.html"><span class="tag">5</span>锁存器/触发器</a>
    <a href="ch06.html"><span class="tag">6</span>时序逻辑电路</a>

    <div class="group-label">存储与可编程</div>
    <a href="ch07.html"><span class="tag">7</span>半导体存储器</a>
    <a href="ch08.html"><span class="tag">8</span>FPGA / CPLD</a>

    <div class="group-label">脉冲与接口</div>
    <a href="ch09.html"><span class="tag">9</span>脉冲波形</a>
    <a href="ch10.html"><span class="tag">10</span>ADC / DAC</a>

    <div class="group-label">专题</div>
    <a href="chips.html"><span class="tag">&#9679;</span>常用芯片专题</a>
    <a href="methods.html"><span class="tag">&#9679;</span>方法汇总</a>
    <a href="index.html" style="margin-top:6px;border-top:1px solid #f1f5f9;padding-top:8px;"><span class="tag">&#8962;</span>返回首页</a>
  </div>
</nav>
<script>
(function(){var p=window.location.pathname.split('/').pop()||'index.html';
document.querySelectorAll('.sidebar-nav a').forEach(function(a){
  if(a.getAttribute('href')===p)a.classList.add('current');
});})();
</script>'''

# Apply to generate_chapters.py template
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace old sidebar CSS
if 'sidebar' in c:
    # Find the old sidebar CSS block
    start = c.find('  /* ===== Left Sidebar ===== */')
    if start >= 0:
        end = c.find('  @media (max-width: 768px)', start)
        # Find the end of the media query
        end = c.find('\n\n', end) if end >= 0 else c.find('.container', start)
        c = c[:start] + sidebar_css.strip() + '\n\n' + c[end:]

    # Replace old sidebar HTML
    old_start = c.find('<nav class="sidebar">')
    if old_start >= 0:
        old_end = c.find('</script>', old_start) + len('</script>')
        c = c[:old_start] + sidebar_html.strip() + c[old_end:]

with open(gen_py, 'w', encoding='utf-8') as f:
    f.write(c)
print("generate_chapters.py: updated")

# Regenerate
os.system(f'cd "{base}" && python generate_chapters.py')

# Update manual pages
for fname in ['ch03.html', 'ch07.html', 'ch10.html', 'chips.html', 'methods.html', 'index.html']:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Replace old sidebar CSS
    if '/* ===== Left Sidebar ===== */' in c:
        start = c.find('/* ===== Left Sidebar ===== */')
        start = c.rfind('\n', 0, start) + 1
        # Find end - look for next media query or section
        end = c.find('@media (max-width: 768px)', start)
        if end >= 0:
            end = c.find('\n', c.find('\n', end) + 1) + 1
        else:
            end = c.find('.container', start)
            end = c.find('\n', end)
        c = c[:start] + sidebar_css.strip() + '\n\n' + c[end:]

    # Replace old sidebar HTML
    old_start = c.find('<nav class="sidebar">')
    if old_start >= 0:
        old_end = c.find('</script>', old_start) + len('</script>')
        c = c[:old_start] + sidebar_html.strip() + c[old_end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"{fname}: updated")

print("All done!")
