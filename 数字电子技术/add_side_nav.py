#!/usr/bin/env python3
"""Add right-side chapter navigation panel to all pages."""
import os

base = "D:/code/cherry studio/复习/数字电子技术"

# The chapter nav panel HTML (insert before </body>)
nav_html = '''
<!-- Right-side chapter nav -->
<button class="chapter-nav-toggle" onclick="toggleChapterNav()" title="章节导航">📖</button>
<div class="chapter-nav-panel" id="chapterNav">
  <div class="nav-title">📂 跳转章节</div>
  <a href="index.html">🏠 首页</a>
  <a href="ch01.html">第1章 数字逻辑概论</a>
  <a href="ch02.html">第2章 逻辑代数</a>
  <a href="ch03.html">第3章 逻辑门电路</a>
  <a href="ch04.html">第4章 组合逻辑</a>
  <a href="ch05.html">第5章 锁存器/触发器</a>
  <a href="ch06.html">第6章 时序逻辑</a>
  <a href="ch07.html">第7章 半导体存储器</a>
  <a href="ch08.html">第8章 FPGA/CPLD</a>
  <a href="ch09.html">第9章 脉冲波形</a>
  <a href="ch10.html">第10章 ADC/DAC</a>
  <a href="chips.html">🔧 芯片专题</a>
  <a href="methods.html">📋 方法汇总</a>
</div>
<script>
function toggleChapterNav() {
  document.getElementById('chapterNav').classList.toggle('open');
}
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

# Update generate_chapters.py template
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the nav panel before </body> in the template
old_footer = '</body>\n</html>'
new_footer = nav_html + '\n</body>\n</html>'
content = content.replace(old_footer, new_footer)

with open(gen_py, 'w', encoding='utf-8') as f:
    f.write(content)
print("generate_chapters.py updated")

# Regenerate auto pages
os.system('cd "' + base + '" && python generate_chapters.py')
print("Auto pages regenerated")

# Now update manual pages: ch03, ch07, ch10, chips, methods, index
manual_files = ['ch03.html', 'ch07.html', 'ch10.html', 'chips.html', 'methods.html', 'index.html']
for fname in manual_files:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'chapter-nav-toggle' in content:
        print(f"{fname}: already has nav, skipping")
        continue
    content = content.replace('</body>', nav_html + '\n</body>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{fname}: updated")

print("All done!")
