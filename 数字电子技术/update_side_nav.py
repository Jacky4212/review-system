#!/usr/bin/env python3
"""Update all pages with improved right-side chapter navigation."""
import os, glob

base = "D:/code/cherry studio/复习/数字电子技术"

# New improved CSS for the side nav (insert before </style>)
nav_css = '''
  /* ===== Right-side Chapter Nav ===== */
  .chapter-nav-toggle {
    position: fixed; right: 0; top: 50%; transform: translateY(-50%);
    width: 40px; height: 40px; border-radius: 10px 0 0 10px;
    background: linear-gradient(135deg, var(--primary), #2a5a8a);
    color: #fff; border: none; font-size: 1.2em; cursor: pointer; z-index: 98;
    opacity: 0.85; transition: all 0.3s ease;
    box-shadow: -3px 0 12px rgba(0,0,0,0.18);
    display: flex; align-items: center; justify-content: center;
  }
  .chapter-nav-toggle:hover { opacity: 1; transform: translateY(-50%) scale(1.08); }
  .chapter-nav-toggle.open { border-radius: 0; }

  .chapter-nav-panel {
    position: fixed; right: -260px; top: 50%; transform: translateY(-50%);
    width: 240px; background: rgba(255,255,255,0.97);
    border-radius: 14px 0 0 14px;
    box-shadow: -6px 0 28px rgba(0,0,0,0.15); z-index: 97;
    transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 16px 0 12px; max-height: 85vh; overflow-y: auto;
    backdrop-filter: blur(8px);
  }
  .chapter-nav-panel.open { right: 0; }

  .chapter-nav-panel .nav-header {
    padding: 0 18px 12px;
    border-bottom: 2px solid var(--accent);
    margin-bottom: 8px;
  }
  .chapter-nav-panel .nav-header .nav-title {
    font-size: 0.95em; font-weight: 700; color: var(--primary);
    letter-spacing: 1px;
  }
  .chapter-nav-panel .nav-header .nav-sub {
    font-size: 0.72em; color: var(--text-light); margin-top: 2px;
  }
  .chapter-nav-panel .nav-section {
    font-size: 0.7em; font-weight: 600; color: var(--text-light);
    padding: 10px 18px 3px; letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .chapter-nav-panel a {
    display: flex; align-items: center; gap: 8px;
    padding: 7px 18px; font-size: 0.88em;
    color: var(--text); text-decoration: none;
    transition: all 0.15s ease;
    border-left: 3px solid transparent;
    margin: 1px 0;
  }
  .chapter-nav-panel a:hover {
    background: linear-gradient(90deg, #e8f4fd, transparent);
    border-left-color: var(--accent);
    color: var(--accent);
  }
  .chapter-nav-panel a.current {
    background: linear-gradient(90deg, #e8f4fd, transparent);
    border-left-color: var(--accent);
    color: var(--accent);
    font-weight: 600;
  }
  .chapter-nav-panel a .num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 5px;
    background: var(--code-bg); font-size: 0.78em; font-weight: 600;
    color: var(--text-light); flex-shrink: 0;
  }
  .chapter-nav-panel a:hover .num { background: var(--accent); color: #fff; }
  .chapter-nav-panel a.current .num { background: var(--accent); color: #fff; }

  .back2top { right: 54px; }
  @media (max-width: 640px) {
    .chapter-nav-panel { width: 200px; font-size: 0.9em; }
    .chapter-nav-panel a { padding: 6px 14px; }
    .back2top { right: 48px; width: 38px; height: 38px; font-size: 1.1em; }
  }
'''

# New improved nav panel HTML
nav_html = '''
<!-- Right-side chapter navigation -->
<button class="chapter-nav-toggle" onclick="toggleChapterNav()" title="章节导航">📖</button>
<div class="chapter-nav-panel" id="chapterNav">
  <div class="nav-header">
    <div class="nav-title">📂 章节导航</div>
    <div class="nav-sub">数字电子技术基础</div>
  </div>

  <div class="nav-section">基础理论</div>
  <a href="ch01.html"><span class="num">1</span> 数字逻辑概论</a>
  <a href="ch02.html"><span class="num">2</span> 逻辑代数与HDL</a>
  <a href="ch03.html"><span class="num">3</span> 逻辑门电路</a>

  <div class="nav-section">组合与时序</div>
  <a href="ch04.html"><span class="num">4</span> 组合逻辑电路</a>
  <a href="ch05.html"><span class="num">5</span> 锁存器/触发器</a>
  <a href="ch06.html"><span class="num">6</span> 时序逻辑电路</a>

  <div class="nav-section">存储与可编程</div>
  <a href="ch07.html"><span class="num">7</span> 半导体存储器</a>
  <a href="ch08.html"><span class="num">8</span> FPGA / CPLD</a>

  <div class="nav-section">脉冲与接口</div>
  <a href="ch09.html"><span class="num">9</span> 脉冲波形</a>
  <a href="ch10.html"><span class="num">10</span> ADC / DAC</a>

  <div class="nav-section">专题</div>
  <a href="chips.html"><span class="num">🔧</span> 常用芯片</a>
  <a href="methods.html"><span class="num">📋</span> 方法汇总</a>
  <a href="index.html"><span class="num">🏠</span> 返回首页</a>
</div>
<script>
function toggleChapterNav() {
  var panel = document.getElementById('chapterNav');
  var btn = document.querySelector('.chapter-nav-toggle');
  panel.classList.toggle('open');
  btn.classList.toggle('open');
}
// Close panel when clicking outside
document.addEventListener('click', function(e) {
  var panel = document.getElementById('chapterNav');
  var btn = document.querySelector('.chapter-nav-toggle');
  if (panel.classList.contains('open') &&
      !panel.contains(e.target) &&
      !btn.contains(e.target)) {
    panel.classList.remove('open');
    btn.classList.remove('open');
  }
});
// Highlight current page
document.addEventListener('DOMContentLoaded', function() {
  var path = window.location.pathname.split('/').pop() || 'index.html';
  var links = document.getElementById('chapterNav').getElementsByTagName('a');
  for (var i = 0; i < links.length; i++) {
    if (links[i].getAttribute('href') === path) {
      links[i].classList.add('current');
    }
  }
});
</script>
'''

# 1. Update template in generate_chapters.py
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace old CSS section
import re
# Find the old nav CSS block and replace it
old_css_start = '  /* Right-side chapter nav panel */'
new_css = nav_css.strip()

if old_css_start in c:
    # Replace from marker to the @media line
    c = re.sub(
        r'  /\* Right-side chapter nav panel \*/\n.*?(?=  @media|\n  \})',
        nav_css.strip() + '\n\n  ',
        c,
        flags=re.DOTALL
    )
else:
    # Add before @media
    c = c.replace(
        '  .back2top:hover { opacity: 1; }',
        '  .back2top:hover { opacity: 1; }\n\n' + nav_css.strip()
    )

# Replace old HTML nav
old_html = '<button class="chapter-nav-toggle" onclick="toggleChapterNav()" title="章节导航">📖</button>\n<div class="chapter-nav-panel" id="chapterNav">\n  <div class="nav-title">📂 跳转章节</div>'
if old_html in c:
    # Find the entire old nav block
    start = c.find(old_html)
    end = c.find('</script>', start) + len('</script>')
    c = c[:start] + nav_html.strip() + c[end:]

with open(gen_py, 'w', encoding='utf-8') as f:
    f.write(c)
print("generate_chapters.py updated")

# 2. Regenerate auto pages
os.system(f'cd "{base}" && python generate_chapters.py')
print("Auto pages regenerated")

# 3. Update manual pages
manual = ['ch03.html', 'ch07.html', 'ch10.html', 'chips.html', 'methods.html', 'index.html']
for fname in manual:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Replace old nav toggle/panel if exists
    if 'chapter-nav-toggle' in c:
        # Remove old nav HTML (from button to </script>)
        old_start = c.find('<!-- Right-side chapter nav -->')
        old_end = c.find('</script>\n', old_start)
        if old_start >= 0 and old_end >= 0:
            old_end += len('</script>\n')
            c = c[:old_start] + nav_html.strip() + '\n' + c[old_end:]
        # Add CSS if missing
        if 'nav-section' not in c:
            c = c.replace('</style>', nav_css + '\n</style>')
        # Fix back2top position
        c = c.replace('.back2top { right: 30px;', '.back2top { right: 54px;')
        c = c.replace('.back2top { right: 50px;', '.back2top { right: 54px;')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"{fname}: updated")

print("All done!")
