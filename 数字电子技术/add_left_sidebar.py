#!/usr/bin/env python3
"""Replace bottom nav-links with fixed left sidebar."""
import os, re

base = "D:/code/cherry studio/复习/数字电子技术"

# CSS for left sidebar
sidebar_css = '''
  /* ===== Left Sidebar ===== */
  .sidebar {
    position: fixed; top: 0; left: 0; width: 200px; height: 100vh;
    background: #f8fafc; border-right: 1px solid #e2e8f0;
    z-index: 100; overflow-y: auto; padding: 16px 0 20px;
  }
  .sidebar .brand { padding: 0 16px 12px; border-bottom: 1px solid #e2e8f0; margin-bottom: 8px; }
  .sidebar .brand .name { font-size: 0.95em; font-weight: 700; color: #1a3a5c; }
  .sidebar .brand .sub { font-size: 0.68em; color: #94a3b8; margin-top: 1px; }
  .sidebar .sec { font-size: 0.62em; font-weight: 600; color: #94a3b8; padding: 10px 16px 3px; letter-spacing: 0.5px; text-transform: uppercase; }
  .sidebar a { display: flex; align-items: center; gap: 6px; padding: 5px 16px; margin: 1px 6px; border-radius: 5px; font-size: 0.8em; color: #334155; text-decoration: none; transition: all 0.12s; }
  .sidebar a:hover { background: #e8f0fe; color: #1a73e8; }
  .sidebar a.current { background: #e8f0fe; color: #1a73e8; font-weight: 600; }
  .sidebar a .tag { display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 4px; background: #e2e8f0; font-size: 0.68em; font-weight: 600; color: #64748b; flex-shrink: 0; }
  .sidebar a:hover .tag { background: #1a73e8; color: #fff; }
  .sidebar a.current .tag { background: #1a73e8; color: #fff; }
  .container { margin-left: 200px; max-width: 900px; }
  .topbar { left: 200px; width: calc(100% - 200px); }
  .footer { margin-left: 200px; }
  @media (max-width: 768px) {
    .sidebar { display: none; }
    .container { margin-left: 0; }
    .topbar { left: 0; width: 100%; }
    .footer { margin-left: 0; }
  }
'''

sidebar_html = '''<nav class="sidebar">
  <div class="brand"><div class="name">数字电子技术</div><div class="sub">复习系统</div></div>
  <div class="sec">基础</div>
  <a href="ch01.html"><span class="tag">1</span>概论</a>
  <a href="ch02.html"><span class="tag">2</span>逻辑代数</a>
  <a href="ch03.html"><span class="tag">3</span>门电路</a>
  <div class="sec">组合与时序</div>
  <a href="ch04.html"><span class="tag">4</span>组合逻辑</a>
  <a href="ch05.html"><span class="tag">5</span>锁存器/触发器</a>
  <a href="ch06.html"><span class="tag">6</span>时序逻辑</a>
  <div class="sec">存储与可编程</div>
  <a href="ch07.html"><span class="tag">7</span>存储器</a>
  <a href="ch08.html"><span class="tag">8</span>FPGA/CPLD</a>
  <div class="sec">脉冲与接口</div>
  <a href="ch09.html"><span class="tag">9</span>脉冲波形</a>
  <a href="ch10.html"><span class="tag">10</span>ADC/DAC</a>
  <div class="sec">专题</div>
  <a href="chips.html"><span class="tag">*</span>芯片</a>
  <a href="methods.html"><span class="tag">*</span>方法汇总</a>
  <a href="index.html"><span class="tag">&#8962;</span>首页</a>
</nav>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var p=window.location.pathname.split('/').pop()||'index.html';
  var a=document.querySelectorAll('.sidebar a');
  for(var i=0;i<a.length;i++){if(a[i].getAttribute('href')===p)a[i].classList.add('current');}
});
</script>'''

# 1. Update generate_chapters.py
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    c = f.read()

# Remove old nav-links from template
c = re.sub(r'  <div class="nav-links">\n.*?\n  </div>', '', c)

# Simplify footer
c = re.sub(r'<p>内容来源: 华中科技大学.*?</p>', '<p>华中科技大学《数字电子技术基础》</p>', c)

# Remove old chapter-nav CSS if any
c = re.sub(r'\n  /\* =====.*?===== \*/.*?(?=\n\n|\n  @)', '', c, flags=re.DOTALL)

# Add sidebar CSS
c = c.replace('</style>', sidebar_css + '\n</style>')

# Add sidebar after <body>
c = c.replace('<body>\n', '<body>\n' + sidebar_html.strip() + '\n')

# Remove old nav-sidebar if any
c = c.replace('<nav class="nav-sidebar"', '<nav class="old-sidebar"')

with open(gen_py, 'w', encoding='utf-8') as f:
    f.write(c)
print("generate_chapters.py: updated")

# Regenerate
os.system(f'cd "{base}" && python generate_chapters.py')

# 2. Update manual pages
for fname in ['ch03.html', 'ch07.html', 'ch10.html', 'chips.html', 'methods.html', 'index.html']:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Remove bottom nav-links
    c = re.sub(r'  <div class="nav-links">\n.*?\n  </div>', '', c)

    # Remove old right-side nav
    c = re.sub(r'<!-- Right-side chapter.*?</script>', '', c, flags=re.DOTALL)
    c = re.sub(r'<nav class="nav-sidebar".*?</script>', '', c, flags=re.DOTALL)

    # Remove old nav CSS
    c = re.sub(r'\n  /\* =====.*?===== \*/.*?(?=\n\n|\n  \})', '', c, flags=re.DOTALL)
    c = re.sub(r'\n  /\* Right-side.*?(?=\n\n|\n  \})', '', c, flags=re.DOTALL)

    # Add sidebar CSS
    if 'sidebar' not in c.split('</style>')[0]:
        c = c.replace('</style>', sidebar_css + '\n</style>')

    # Add sidebar
    if 'class="sidebar"' not in c:
        c = c.replace('<body>\n', '<body>\n' + sidebar_html.strip() + '\n')

    # Simplify footer
    c = re.sub(r'<p>内容来源: 华中科技大学.*?</p>', '<p>华中科技大学《数字电子技术基础》</p>', c)

    # Remove old sidebar classes
    c = c.replace('class="nav-sidebar"', 'class="old-sidebar"')
    c = c.replace('class="sidebar-toggle"', 'class="old-toggle"')
    c = c.replace('class="sidebar-overlay"', 'class="old-overlay"')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"{fname}: updated")

print("All done!")
