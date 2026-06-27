#!/usr/bin/env python3
"""Update ch02 content in generate_chapters.py to match ch02.html."""
path = 'D:/code/cherry studio/复习/数字电子技术/generate_chapters.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old = '''  <div class="section">
    <h2>2.2 逻辑函数表达式的形式</h2>
    <h3>最小项</h3>
    <p>n个变量的最小项是n个因子的乘积，每个变量都以它的原变量或非变量的形式在乘积项中出现，且仅出现一次。n个变量的最小项应有2<sup>n</sup>个。</p>
    <p>最小项的性质：</p>
    <ul>
      <li>对于任意一个最小项，只有一组变量取值使得它的值为1</li>
      <li>任意两个最小项的乘积为0</li>
      <li>全体最小项之和为1</li>
    </ul>
    <h3>最大项</h3>
    <p>n个变量的最大项是n个因子或相，每个变量都以它的原变量或非变量的形式在或项中出现，且仅出现一次。</p>
  </div>'''

new = '''  <div class="section">
    <h2>2.2 逻辑函数表达式的形式</h2>

    <h3>最小项与最大项的定义</h3>
    <p><strong>最小项：</strong>n个变量的最小项是n个因子的<strong>乘积</strong>，每个变量都以它的原变量或非变量的形式在乘积项中出现，且仅出现一次。n个变量的最小项应有2<sup>n</sup>个。</p>
    <p><strong>最大项：</strong>n个变量的最大项是n个因子<strong>或相</strong>，每个变量都以它的原变量或非变量的形式在或项中出现，且仅出现一次。n个变量的最大项应有2<sup>n</sup>个。</p>

    <h3>最小项与最大项对照</h3>
    <table>
      <tr><th>比较项</th><th>最小项（Σm）</th><th>最大项（ΠM）</th></tr>
      <tr><td><strong>形式</strong></td><td>乘积项（与）</td><td>或项（或）</td></tr>
      <tr><td><strong>记法</strong></td><td>m<sub>i</sub></td><td>M<sub>i</sub></td></tr>
      <tr><td><strong>表达式</strong></td><td>Σm（相加）</td><td>ΠM（相乘）</td></tr>
      <tr><td><strong>取值</strong></td><td>仅一组使之为<strong>1</strong></td><td>仅一组使之为<strong>0</strong></td></tr>
      <tr><td><strong>两两关系</strong></td><td>任意两个之<strong>积</strong>为0</td><td>任意两个之<strong>和</strong>为1</td></tr>
      <tr><td><strong>全体</strong></td><td>全体之<strong>和</strong>为1</td><td>全体之<strong>积</strong>为0</td></tr>
      <tr><td><strong>编号关系</strong></td><td colspan="2">m<sub>i</sub> = <span style="text-decoration:overline">M</span><sub>i</sub>，M<sub>i</sub> = <span style="text-decoration:overline">m</span><sub>i</sub></td></tr>
      <tr><td><strong>变量=0时</strong></td><td>反变量（如<span style="text-decoration:overline">A</span>）</td><td>原变量（如A）</td></tr>
      <tr><td><strong>变量=1时</strong></td><td>原变量（如A）</td><td>反变量（如<span style="text-decoration:overline">A</span>）</td></tr>
    </table>

    <h3>最小项表达式与最大项表达式的转换</h3>
    <p>对于函数 F = AB + <span style="text-decoration:overline">A</span>C：</p>
    <ul>
      <li><strong>最小项表达式（看F=1）：</strong>F = Σm(1, 3, 6, 7) = <span style="text-decoration:overline">A</span><span style="text-decoration:overline">B</span>C + <span style="text-decoration:overline">A</span>BC + AB<span style="text-decoration:overline">C</span> + ABC</li>
      <li><strong>最大项表达式（看F=0）：</strong>F = ΠM(0, 2, 4, 5) = (A+B+C)(A+<span style="text-decoration:overline">B</span>+C)(<span style="text-decoration:overline">A</span>+B+C)(<span style="text-decoration:overline">A</span>+B+<span style="text-decoration:overline">C</span>)</li>
    </ul>
    <p>两种表达式可以通过真值表相互转换：取F=1的项得最小项表达式，取F=0的项得最大项表达式。</p>
  </div>'''

if old in c:
    c = c.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('not found')
