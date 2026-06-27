#!/usr/bin/env python3
"""Generate clean chapter pages with manually curated key content."""
import os

PAGE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第CHAPTER_NUM章 CHAPTER_TITLE - 数字电子技术</title>
<style>
  :root {
    --primary: #1a3a5c; --accent: #2d7fc1; --bg: #f5f7fa; --card-bg: #ffffff;
    --text: #2c3e50; --text-light: #7f8c8d; --border: #e1e8ed; --code-bg: #f0f4f8;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.8;
  }
  .topbar {
    background: linear-gradient(135deg, var(--primary), var(--accent)); color: #fff; padding: 20px;
    position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }
  .topbar-inner {
    max-width: 1100px; margin: 0 auto;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
  }
  .topbar a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.9em; }
  .topbar a:hover { color: #fff; }
  .topbar h2 { font-size: 1.2em; }
  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }
  .section {
    background: var(--card-bg); border-radius: 12px; padding: 30px; margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .section h2 {
    font-size: 1.4em; color: var(--primary); border-left: 4px solid var(--accent);
    padding-left: 14px; margin-bottom: 20px;
  }
  .section h3 {
    font-size: 1.15em; color: var(--accent); margin: 20px 0 10px;
    padding-bottom: 6px; border-bottom: 1px dashed var(--border);
  }
  .section h4 { font-size: 1em; color: var(--text); margin: 14px 0 6px; font-weight: 600; }
  .section p { margin-bottom: 10px; }
  .section ul { margin: 8px 0 14px 22px; }
  .section li { margin-bottom: 6px; }
  .highlight {
    background: #fffbe6; border-left: 3px solid #f0c040;
    padding: 12px 16px; margin: 14px 0; border-radius: 6px; font-size: 0.95em;
  }
  .highlight strong { color: #c0392b; }
  .def-box {
    background: var(--code-bg); border-radius: 8px; padding: 14px 18px; margin: 12px 0; font-size: 0.95em;
  }
  .def-box strong { color: var(--accent); }
  .nav-links { margin-top: 30px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
  .nav-links a {
    display: inline-block; padding: 10px 24px; background: var(--card-bg); border-radius: 8px;
    text-decoration: none; color: var(--accent); border: 1px solid var(--border);
    transition: all 0.2s; font-size: 0.95em;
  }
  .nav-links a:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
  .back2top {
    position: fixed; bottom: 30px; right: 30px; width: 44px; height: 44px; border-radius: 50%;
    background: var(--primary); color: #fff; border: none; font-size: 1.4em; cursor: pointer;
    opacity: 0.7; transition: opacity 0.2s; z-index: 99; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
  .back2top:hover { opacity: 1; }
  table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 0.93em; }
  th, td { border: 1px solid var(--border); padding: 7px 10px; text-align: center; }
  th { background: var(--code-bg); font-weight: 600; color: var(--primary); }
  .footer { text-align: center; padding: 24px; color: var(--text-light); font-size: 0.85em; border-top: 1px solid var(--border); }
  @media (max-width: 640px) { .section { padding: 20px 16px; } .topbar h2 { font-size: 1em; } }
</style>
</head>
<body>
<div class="topbar">
  <div class="topbar-inner">
    <a href="TOPBAR_PREV">TOPBAR_PREV_LABEL</a>
    <h2>第CHAPTER_NUM章 CHAPTER_TITLE</h2>
    <a href="TOPBAR_NEXT">TOPBAR_NEXT_LABEL</a>
  </div>
</div>
<div class="container">
CONTENT
  <div class="nav-links">
    <a href="index.html">← 返回首页</a>
    <a href="NAV_PREV">NAV_PREV_LABEL</a>
    <a href="NAV_NEXT">NAV_NEXT_LABEL</a>
  </div>
</div>
<button class="back2top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>
<div class="footer">
  <p>内容来源: 华中科技大学《数字电子技术基础》课程PPT · 第CHAPTER_NUM章 CHAPTER_TITLE</p>
</div>
</body>
</html>'''

CHAPTERS = [
    {
        'num': '1', 'file': 'ch01', 'title': '数字逻辑概论',
        'prev': 'index.html', 'prev_label': '课程首页',
        'next': 'ch02.html', 'next_label': '第2章 逻辑代数与HDL基础 →',
        'tprev': 'index.html', 'tprev_label': '← 返回首页',
        'tnext': 'ch02.html', 'tnext_label': '第2章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>了解数字信号与数字电路的基本概念</li>
      <li>了解数字信号的特点及表示方法</li>
      <li>掌握常用二～十、二～十六进制数的转换</li>
      <li>熟悉常用二进制码：8421 BCD码、格雷码</li>
      <li>掌握基本逻辑运算及逻辑函数的表示方法</li>
    </ul>
  </div>

  <div class="section">
    <h2>1.1 数字信号与数字电路</h2>
    <p><strong>模拟信号</strong>：时间和数值均连续变化的电信号，如正弦波、三角波等。</p>
    <p><strong>数字信号</strong>：在时间上和数值上均是离散的信号。</p>
    <p>数字电路可分为<strong>组合逻辑电路</strong>和<strong>时序逻辑电路</strong>。</p>
    <p>数字电路从集成度不同可分为：小规模(SSI)、中规模(MSI)、大规模(LSI)、超大规模(VLSI)和甚大规模(ULSI)五类。</p>
    <p>数字集成电路的特点：稳定性高抗干扰能力强、易于设计、体积小通用性好、具可编程性及保密性、高速度低功耗、可扩展性。</p>
  </div>

  <div class="section">
    <h2>1.2 数制</h2>
    <p><strong>数制</strong>：多位数码中的每一位数的构成及低位向高位进位的规则。</p>
    <h3>十进制</h3>
    <p>采用0~9十个数码，进位规则是"逢十进一"。</p>
    <h3>二进制</h3>
    <p>只有0、1两个数码，进位规律是："逢二进一"。各位的权都是2的幂。</p>
    <p>二进制的优点：(1)易于电路表达 (2)所用元件少，电路简单可靠 (3)基本运算规则简单。</p>
    <h3>二-十进制转换</h3>
    <p><strong>整数转换（辗转相除法）</strong>：将十进制数连续不断地除以2，直至商为零，所得余数由低位到高位排列。</p>
    <p><strong>小数转换（基数乘法）</strong>：将十进制小数每次除去上次所得积中的整数再乘以2，直到满足误差要求。</p>
    <h3>十六进制</h3>
    <p>有0~9、A~F十六个数码，进位规律是"逢十六进一"。各位的权均为16的幂。</p>
    <p>十六进制的优点：(1)与二进制之间的转换容易 (2)计数容量较其它进制都大 (3)书写简洁。</p>
  </div>

  <div class="section">
    <h2>1.3 二进制数的算术运算</h2>
    <p>加法规则：0+0=0，0+1=1，1+1=10</p>
    <p>减法规则：0-0=0，1-1=0，1-0=1，0-1=11（借位）</p>
    <p>有符号二进制数用最高位表示符号位，0表示正数，1表示负数。</p>
    <div class="def-box">
      <strong>补码表示：</strong>正数的补码与原码相同。负数的补码：将原码的数值位逐位求反，然后在最低位加1。<br>
      减法运算原理：A − B = A + (−B)，对(−B)求补码，然后进行加法运算。
    </div>
    <p><strong>溢出判别</strong>：如果两个加数的符号相同，而和的符号与它们不同，则运算结果是错误的，产生溢出。</p>
  </div>

  <div class="section">
    <h2>1.4 二进制代码</h2>
    <p><strong>码制</strong>：编制代码所要遵循的规则。</p>
    <p>二进制代码的位数n与需要编码的事件个数N之间应满足：2<sup>n-1</sup> ≤ N ≤ 2<sup>n</sup></p>
    <h3>常用BCD码</h3>
    <table>
      <tr><th>十进制</th><th>8421码</th><th>2421码</th><th>5421码</th><th>余3码</th><th>余3循环码</th></tr>
      <tr><td>0</td><td>0000</td><td>0000</td><td>0000</td><td>0011</td><td>0010</td></tr>
      <tr><td>1</td><td>0001</td><td>0001</td><td>0001</td><td>0100</td><td>0110</td></tr>
      <tr><td>2</td><td>0010</td><td>0010</td><td>0010</td><td>0101</td><td>0111</td></tr>
      <tr><td>3</td><td>0011</td><td>0011</td><td>0011</td><td>0110</td><td>0101</td></tr>
      <tr><td>4</td><td>0100</td><td>0100</td><td>0100</td><td>0111</td><td>0100</td></tr>
      <tr><td>5</td><td>0101</td><td>1011</td><td>1000</td><td>1000</td><td>1100</td></tr>
      <tr><td>6</td><td>0110</td><td>1100</td><td>1001</td><td>1001</td><td>1101</td></tr>
      <tr><td>7</td><td>0111</td><td>1101</td><td>1010</td><td>1010</td><td>1111</td></tr>
      <tr><td>8</td><td>1000</td><td>1110</td><td>1011</td><td>1011</td><td>1110</td></tr>
      <tr><td>9</td><td>1001</td><td>1111</td><td>1100</td><td>1100</td><td>1010</td></tr>
    </table>
    <h3>格雷码</h3>
    <p>特点是：任何两个相邻代码之间<strong>仅有一位取值不同</strong>。格雷码是一种常见的无权码，又称为<strong>循环码</strong>。</p>
    <p>格雷码是错误最小化的编码。当模拟量发生微小变化，格雷码仅仅改变一位，更加可靠且容易检错。</p>
  </div>

  <div class="section">
    <h2>1.5 二值逻辑变量与基本逻辑运算</h2>
    <p><strong>逻辑运算</strong>：当0和1表示逻辑状态时，两个二进制数码按照某种特定的因果关系进行的运算。</p>
    <p>逻辑运算使用的数学工具是<strong>逻辑代数</strong>。有与、或、非三种基本逻辑运算。</p>
    <ul>
      <li><strong>与运算</strong>（L = A · B = AB）：只有当决定某一事件的条件全部具备时，这一事件才会发生。</li>
      <li><strong>或运算</strong>（L = A + B）：只要有一个或几个条件具备时，事件就会发生。</li>
      <li><strong>非运算</strong>（L = <span style="text-decoration:overline">A</span> = ¬A = A'）：条件具备时事件不发生，条件不具备时事件发生。</li>
      <li><strong>与非运算</strong>（L = <span style="text-decoration:overline">A·B</span> = <span style="text-decoration:overline">A</span>+<span style="text-decoration:overline">B</span>）：先与后非，输入全1时输出0。与-或表达式转换可用摩根定律。</li>
      <li><strong>或非运算</strong>（L = <span style="text-decoration:overline">A+B</span> = <span style="text-decoration:overline">A</span>·<span style="text-decoration:overline">B</span>）：先或后非，输入全0时输出1。与-或表达式转换可用摩根定律。</li>
      <li><strong>异或运算</strong>（L = A ⊕ B = <span style="text-decoration:overline">A</span>·B + A·<span style="text-decoration:overline">B</span>）：两个输入变量的值相异，输出为1，否则为0。</li>
      <li><strong>同或运算</strong>（L = A ⊙ B = <span style="text-decoration:overline">A⊕B</span> = A·B + <span style="text-decoration:overline">A</span>·<span style="text-decoration:overline">B</span>）：两个输入变量的值相同，输出为1，否则为0。</li>
    </ul>
  </div>

  <div class="section">
    <h2>1.6 逻辑函数及其表示方法</h2>
    <p>逻辑函数有五种表示方法：</p>
    <ul>
      <li><strong>真值表</strong>：列出所有输入组合对应的输出值</li>
      <li><strong>逻辑表达式</strong>：用与、或、非等运算组合表示</li>
      <li><strong>逻辑图</strong>：用逻辑符号表示逻辑关系</li>
      <li><strong>波形图</strong>：用输入输出信号的波形表示</li>
      <li><strong>卡诺图</strong>：用方格图表示（见第2章）</li>
    </ul>
    <p>这些表示方法之间可以相互转换。</p>
  </div>
'''
    },
    {
        'num': '2', 'file': 'ch02', 'title': '逻辑代数与HDL基础',
        'prev': 'ch01.html', 'prev_label': '← 第1章 数字逻辑概论',
        'next': 'ch03.html', 'next_label': '第3章 逻辑门电路 →',
        'tprev': 'ch01.html', 'tprev_label': '← 第1章',
        'tnext': 'ch03.html', 'tnext_label': '第3章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>熟悉逻辑代数常用基本定律、恒等式和规则</li>
      <li>掌握逻辑代数的表示方法</li>
      <li>掌握逻辑代数的变换和卡诺图化简法</li>
      <li>熟悉硬件描述语言Verilog HDL</li>
    </ul>
  </div>

  <div class="section">
    <h2>2.1 逻辑代数的基本定律和规则</h2>
    <p>逻辑代数又称<strong>布尔代数</strong>，是分析和设计现代数字逻辑电路不可缺少的数学工具。</p>
    <h3>基本公式</h3>
    <ul>
      <li>0-1律：A·0=0，A+1=1</li>
      <li>自等律：A·1=A，A+0=A</li>
      <li>互补律：A·<span style="text-decoration:overline">A</span>=0，A+<span style="text-decoration:overline">A</span>=1</li>
      <li>重叠律：A·A=A，A+A=A</li>
      <li>交换律：A·B=B·A，A+B=B+A</li>
      <li>结合律：A·(B·C)=(A·B)·C，A+(B+C)=(A+B)+C</li>
      <li>分配律：A·(B+C)=AB+AC，A+BC=(A+B)(A+C)</li>
      <li>吸收律：A+AB=A，A·(A+B)=A</li>
      <li>摩根定律：<span style="text-decoration:overline">(A·B)</span>=<span style="text-decoration:overline">A</span>+<span style="text-decoration:overline">B</span>，<span style="text-decoration:overline">(A+B)</span>=<span style="text-decoration:overline">A</span>·<span style="text-decoration:overline">B</span></li>
    </ul>
    <h3>基本规则</h3>
    <ul>
      <li><strong>代入规则</strong>：在包含变量A逻辑等式中，如果用另一个函数式代入式中所有A的位置，则等式仍然成立。</li>
      <li><strong>反演规则</strong>：将逻辑表达式L中所有·换成+，+换成·；原变量换反变量，反变量换原变量；1换0，0换1；得到的结果就是原函数的反函数。</li>
      <li><strong>对偶规则</strong>：若某个逻辑恒等式成立，则该恒等式两侧的对偶式也相等。</li>
    </ul>
  </div>

  <div class="section">
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
  </div>

  <div class="section">
    <h2>2.3 逻辑函数的代数化简法</h2>
    <p>化简的目的：降低电路实现的成本，以较少的门实现电路。</p>
    <p><strong>最简与-或表达式</strong>：包含的与项数最少，且每个与项中变量数最少。</p>
    <p>化简方法：</p>
    <ul>
      <li><strong>并项法</strong>：利用A+<span style="text-decoration:overline">A</span>=1合并两项</li>
      <li><strong>吸收法</strong>：利用A+AB=A吸收多余项</li>
      <li><strong>消去法</strong>：利用A+<span style="text-decoration:overline">A</span>B=A+B消去多余因子</li>
      <li><strong>配项法</strong>：通过配项简化表达式</li>
    </ul>
  </div>

  <div class="section">
    <h2>2.4 卡诺图化简法</h2>
    <p><strong>卡诺图</strong>：将n变量的全部最小项都用小方块表示，并使具有<strong>逻辑相邻</strong>的最小项在几何位置上也相邻地排列起来。</p>
    <p>逻辑相邻的最小项：如果两个最小项只有一个变量互为反变量，就称这两个最小项在逻辑上相邻。</p>
    <p>化简步骤：</p>
    <ul>
      <li>将逻辑函数写成最小项表达式</li>
      <li>按最小项表达式填卡诺图，含最小项的方格填1，其余填0</li>
      <li>合并相邻的1方格圈成一组（包围圈），每组含2<sup>n</sup>个方格</li>
      <li>将所有包围圈对应的乘积项相加</li>
    </ul>
    <div class="highlight">
      <strong>💡 无关项：</strong>在真值表内对应于变量的某些取值下，函数的值可以是任意的，或者这些变量的取值根本不会出现。化简中它的值可以取0或1，根据使函数尽量简化而定。
    </div>
  </div>

  <div class="section">
    <h2>2.5 Verilog HDL基础</h2>
    <p><strong>硬件描述语言HDL</strong>：以文本形式来描述数字系统硬件的结构和行为的语言。</p>
    <p>模块是Verilog描述电路的基本单元。每个模块以<strong>module</strong>开始，以<strong>endmodule</strong>结束。</p>
    <p>逻辑功能的描述方式有三种：</p>
    <ul>
      <li><strong>结构描述方式</strong>（门级描述）</li>
      <li><strong>数据流描述方式</strong>（assign语句）</li>
      <li><strong>行为描述方式</strong>（always语句）</li>
    </ul>
    <p>Verilog有4种基本逻辑值：0（逻辑0/假）、1（逻辑1/真）、x（不确定）、z（高阻态）。</p>
    <p>数据类型：<strong>线网类型（wire）</strong>输出始终根据输入的变化而更新；<strong>变量类型（reg）</strong>对应具有状态保持作用的电路元件。</p>
  </div>
'''
    },
    {
        'num': '4', 'file': 'ch04', 'title': '组合逻辑电路',
        'prev': 'ch03.html', 'prev_label': '← 第3章 逻辑门电路',
        'next': 'ch05.html', 'next_label': '第5章 锁存器和触发器 →',
        'tprev': 'ch03.html', 'tprev_label': '← 第3章',
        'tnext': 'ch05.html', 'tnext_label': '第5章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>熟练掌握组合逻辑电路的分析方法和设计方法</li>
      <li>掌握编码器、译码器、数据选择器、数值比较器和加法器的逻辑功能及其应用</li>
      <li>学会阅读器件的功能表，并能根据设计要求完成电路的正确连接</li>
      <li>掌握可编程逻辑器件的表示方法，会用PLD实现组合逻辑电路</li>
    </ul>
  </div>

  <div class="section">
    <h2>4.1 组合逻辑电路的分析</h2>
    <div class="def-box">
      <strong>组合逻辑电路工作特点：</strong>在任何时刻，电路的输出状态只取决于同一时刻的输入状态而与电路原来的状态无关。<br>
      <strong>结构特征：</strong>输出输入之间没有反馈延迟通路，不含记忆单元。
    </div>
    <p>分析步骤：</p>
    <ul>
      <li>由逻辑图写出各输出端的逻辑表达式</li>
      <li>化简和变换逻辑表达式</li>
      <li>列出真值表</li>
      <li>根据真值表或逻辑表达式，确定其功能</li>
    </ul>
  </div>

  <div class="section">
    <h2>4.2 组合逻辑电路的设计</h2>
    <p>设计步骤：</p>
    <ul>
      <li>逻辑抽象：根据实际逻辑问题的因果关系确定输入、输出变量</li>
      <li>根据逻辑描述列出真值表</li>
      <li>由真值表写出逻辑表达式</li>
      <li>简化和变换逻辑表达式，画出逻辑图</li>
    </ul>
  </div>

  <div class="section">
    <h2>4.3 竞争冒险</h2>
    <p><strong>竞争</strong>：当一个逻辑门的两个输入端的信号同时向相反方向变化，而变化的时间有差异的现象。</p>
    <p><strong>冒险</strong>：两个输入端的信号取值的变化方向相反时，由竞争可能产生输出干扰脉冲的现象。</p>
    <p>消去竞争冒险的方法：</p>
    <ul>
      <li>发现并消除互补变量</li>
      <li>增加乘积项，避免互补项相加</li>
      <li>输出端并联电容器（慢速工作时）</li>
    </ul>
  </div>

  <div class="section">
    <h2>4.4 常用组合逻辑电路模块</h2>
    <h3>编码器</h3>
    <p><strong>编码</strong>：赋予二进制代码特定含义的过程。具有编码功能的逻辑电路称为编码器。</p>
    <p><strong>优先编码器</strong>：允许同时输入两个以上的有效编码信号，能按预先设定的优先级别，只对其中优先权最高的一个进行编码。</p>

    <h3>译码器</h3>
    <p><strong>译码</strong>是编码的逆过程，能将二进制码翻译成代表某一特定含义的信号。</p>
    <p><strong>74HC138</strong>是3线-8线二进制译码器，3个输入端A<sub>2</sub>A<sub>1</sub>A<sub>0</sub>（高有效），8个输出端Y<sub>0</sub>~Y<sub>7</sub>（低有效）。详见<a href="chips.html">芯片专题</a>。</p>

    <h3>数据选择器</h3>
    <p>在通道选择信号的作用下，将多个通道的数据分时传送到公共的数据通道上去。</p>

    <h3>数值比较器</h3>
    <p>对两个二进制数进行比较，以判断其大小的逻辑电路。</p>

    <h3>加法器</h3>
    <ul>
      <li><strong>半加器</strong>：不考虑低位进位，将两个1位二进制数相加。</li>
      <li><strong>全加器</strong>：考虑低位进位信号的加法。</li>
      <li><strong>超前进位加法器</strong>：设计进位信号产生电路，在输入每位的加数和被加数时，同时获得该位全加的进位信号，无需等待最低位的进位信号。</li>
    </ul>
  </div>
'''
    },
    {
        'num': '5', 'file': 'ch05', 'title': '锁存器和触发器',
        'prev': 'ch04.html', 'prev_label': '← 第4章 组合逻辑电路',
        'next': 'ch06.html', 'next_label': '第6章 时序逻辑电路 →',
        'tprev': 'ch04.html', 'tprev_label': '← 第4章',
        'tnext': 'ch06.html', 'tnext_label': '第6章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>掌握锁存器、触发器的电路结构和工作原理</li>
      <li>熟练掌握SR触发器、JK触发器、D触发器及T触发器的逻辑功能</li>
      <li>正确理解锁存器、触发器的动态特性</li>
    </ul>
  </div>

  <div class="section">
    <h2>概述</h2>
    <p>锁存器和触发器是构成时序逻辑电路的基本逻辑单元。</p>
    <div class="def-box">
      <strong>共同点：</strong>具有0和1两个稳定状态，一旦状态被确定，就能自行保持。一个锁存器或触发器能存储一位二进制码。<br>
      <strong>不同点：</strong><br>
      • <strong>锁存器</strong>——对脉冲电平敏感的存储电路，在特定输入脉冲电平作用下改变状态。<br>
      • <strong>触发器</strong>——对脉冲边沿敏感的存储电路，在时钟脉冲的上升沿或下降沿的变化瞬间改变状态。
    </div>
  </div>

  <div class="section">
    <h2>5.1 基本双稳态电路</h2>
    <p>两个反相器交叉耦合构成最基本的双稳态电路。电路具有记忆1位二进制数据的功能。Q端的状态定义为电路输出状态。</p>
  </div>

  <div class="section">
    <h2>5.2 SR锁存器</h2>
    <p>SR锁存器（Set-Reset Latch）由两个或非门（或与非门）交叉耦合构成。</p>
    <table>
      <tr><th>R</th><th>S</th><th>Q<sup>n+1</sup></th><th>功能</th></tr>
      <tr><td>0</td><td>0</td><td>Q<sup>n</sup></td><td>保持</td></tr>
      <tr><td>0</td><td>1</td><td>1</td><td>置1</td></tr>
      <tr><td>1</td><td>0</td><td>0</td><td>置0</td></tr>
      <tr><td>1</td><td>1</td><td>不确定</td><td>禁止</td></tr>
    </table>
    <p>约束条件：<strong>SR = 0</strong>（S和R不能同时为1）</p>
  </div>

  <div class="section">
    <h2>5.3 D锁存器</h2>
    <p>D锁存器在E=1时Q=D（跟随），E=0时Q不变（保持）。</p>
    <p>由传输门构成的D锁存器：E=1时TG1导通TG2断开，Q=D；E=0时TG1断开TG2导通，Q不变。</p>
  </div>

  <div class="section">
    <h2>5.4 D触发器（边沿触发）</h2>
    <p>主从D触发器由主锁存器和从锁存器构成，在CP的上升沿将D端信号传送到输出端。</p>
    <p>触发器的状态仅仅取决于CP信号上升沿到达前瞬间的D信号。</p>
  </div>

  <div class="section">
    <h2>5.5 触发器的逻辑功能</h2>
    <h3>D触发器</h3>
    <p>特性方程：<strong>Q<sup>n+1</sup> = D</strong></p>
    <h3>JK触发器</h3>
    <p>特性方程：<strong>Q<sup>n+1</sup> = J·<span style="text-decoration:overline">Q</span><sup>n</sup> + <span style="text-decoration:overline">K</span>·Q<sup>n</sup></strong></p>
    <h3>T触发器</h3>
    <p>特性方程：<strong>Q<sup>n+1</sup> = T ⊕ Q<sup>n</sup></strong></p>
    <p>当T=1时，称为T′触发器，时钟脉冲每作用一次，触发器翻转一次（二分频）。</p>
    <h3>SR触发器</h3>
    <p>特性方程：<strong>Q<sup>n+1</sup> = S + <span style="text-decoration:overline">R</span>·Q<sup>n</sup></strong>（约束条件SR=0）</p>
    <div class="highlight">
      <strong>💡 触发器的电路结构与逻辑功能没有必然联系。</strong>
    </div>
  </div>
'''
    },
    {
        'num': '6', 'file': 'ch06', 'title': '时序逻辑电路',
        'prev': 'ch05.html', 'prev_label': '← 第5章 锁存器和触发器',
        'next': 'ch07.html', 'next_label': '第7章 半导体存储器 →',
        'tprev': 'ch05.html', 'tprev_label': '← 第5章',
        'tnext': 'ch07.html', 'tnext_label': '第7章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>熟练掌握时序逻辑电路的描述方式及其相互转换</li>
      <li>熟练掌握时序逻辑电路的分析方法</li>
      <li>熟练掌握时序逻辑电路的设计方法</li>
      <li>熟练掌握常用时序逻辑电路计数器、寄存器、移位寄存器的逻辑功能及其应用</li>
      <li>熟悉时序逻辑的可编程电路实现原理</li>
    </ul>
  </div>

  <div class="section">
    <h2>6.1 时序逻辑电路的基本概念</h2>
    <div class="def-box">
      <strong>结构特征：</strong>电路由组合电路和存储电路组成，存在反馈。<br>
      <strong>工作特征：</strong>任意时刻的输出状态不仅与该当前的输入信号有关，而且与此前电路的状态有关。
    </div>
    <p>时序电路的三种方程：</p>
    <ul>
      <li><strong>输出方程</strong>：O = f<sub>1</sub>(I, S)</li>
      <li><strong>激励方程</strong>：E = f<sub>2</sub>(I, S)</li>
      <li><strong>状态转换方程</strong>：S<sup>n+1</sup> = f<sub>3</sub>(E, S<sup>n</sup>)</li>
    </ul>
    <p>时序电路的五种描述方式（可相互转换）：逻辑方程组、状态转换表、状态转换图、时序图、波形图。</p>
  </div>

  <div class="section">
    <h2>6.2 同步时序逻辑电路的分析</h2>
    <p>同步时序逻辑电路分析的任务：分析电路在输入信号作用下，其状态和输出信号变化的规律，进而确定电路的逻辑功能。</p>
    <p>分析步骤：</p>
    <ul>
      <li>了解电路的组成（输入、输出信号、触发器类型等）</li>
      <li>写出输出方程、各触发器的激励方程、状态转换方程</li>
      <li>列出状态转换表或画出状态转换图、波形图</li>
      <li>确定电路的逻辑功能</li>
    </ul>
  </div>

  <div class="section">
    <h2>6.3 同步时序逻辑电路的设计</h2>
    <p>设计是分析的逆过程。步骤：</p>
    <ul>
      <li>根据给定的逻辑功能建立原始状态转换图和原始状态转换表</li>
      <li>状态化简——合并等价状态，消去多余状态</li>
      <li>状态编码（状态分配）</li>
      <li>选择触发器的类型</li>
      <li>求出电路的激励方程和输出方程</li>
      <li>画出逻辑图并检查自启动能力</li>
    </ul>
  </div>

  <div class="section">
    <h2>6.4 异步时序逻辑电路的分析</h2>
    <p>分析时必须考虑各触发器的时钟信号作用情况。每一次状态转换必须从输入信号所能触发的第一个触发器开始逐级确定。</p>
  </div>

  <div class="section">
    <h2>6.5 常用时序逻辑电路模块</h2>
    <h3>寄存器</h3>
    <p>寄存器是数字系统中用来存储代码或数据的逻辑部件。一个触发器能存储1位二进制代码，存储n位二进制代码需用n个触发器。</p>
    <h3>移位寄存器</h3>
    <p>既能寄存数码，又能在时钟脉冲的作用下使数码向高位或向低位移动。</p>
    <h3>计数器</h3>
    <p>计数器的基本功能是对输入时钟脉冲进行计数。也可用于分频、定时、产生节拍脉冲等。</p>
    <p><strong>74LVC161</strong>是4位二进制同步加计数器，具有异步清零和同步并行置数功能。详见<a href="chips.html">芯片专题</a>。</p>
  </div>
'''
    },
    {
        'num': '8', 'file': 'ch08', 'title': 'FPGA和CPLD',
        'prev': 'ch07.html', 'prev_label': '← 第7章 半导体存储器',
        'next': 'ch09.html', 'next_label': '第9章 脉冲波形的变换与产生 →',
        'tprev': 'ch07.html', 'tprev_label': '← 第7章',
        'tnext': 'ch09.html', 'tnext_label': '第9章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>了解现场可编程门阵列（FPGA）实现逻辑功能的原理、结构与使用特点</li>
      <li>了解复杂可编程逻辑器件（CPLD）的结构</li>
      <li>了解现代EDA工具及开发流程</li>
    </ul>
  </div>

  <div class="section">
    <h2>概述</h2>
    <p>CPLD用可编程"与-或"阵列实现逻辑函数。编程基于E<sup>2</sup>PROM或快闪存储器。</p>
    <p>FPGA是用<strong>查找表LUT</strong>实现逻辑函数。复杂函数使用众多的LUT和触发器实现。编程基于<strong>SRAM</strong>。</p>
    <p>CPLD的电路规模和灵活性不如FPGA，但<strong>可加密</strong>。</p>
  </div>

  <div class="section">
    <h2>8.1 FPGA</h2>
    <h3>LUT（查找表）</h3>
    <p>LUT是FPGA实现逻辑函数的基本单元。LUT实质是一个小规模的存储器，以真值表的形式实现给定的逻辑函数。</p>
    <p>目前FPGA中的LUT大多是4~6个输入，1个输出。当变量数超过一个LUT的输入数时，需要将多个LUT扩展使用。</p>

    <h3>FPGA结构</h3>
    <p>FPGA包括三个主要部分：</p>
    <ul>
      <li><strong>可编程逻辑块</strong>——包含LUT和触发器，可实现组合逻辑、时序逻辑、加法器等</li>
      <li><strong>可编程互联开关</strong>——实现逻辑块之间、逻辑块与I/O之间的连接</li>
      <li><strong>可编程I/O模块</strong>——将引脚编程为输入、输出和双向功能</li>
    </ul>
  </div>

  <div class="section">
    <h2>8.2 CPLD</h2>
    <p>CPLD器件内部含有多个逻辑块，每个逻辑块都相当于一个PAL器件。每个块之间使用可编程内部连线实现相互连接。</p>
    <p>宏单元包含一个或门、一个触发器和一些可编程的数据选择器及控制门。</p>
    <p>查找表CPLD是将FPGA的LUT与<strong>非易失性存储器</strong>（FLASH）相结合：上电时将FLASH的信息加载到LUT的SRAM中。</p>
  </div>

  <div class="section">
    <h2>8.3 可编程逻辑器件开发过程</h2>
    <p>开发流程：</p>
    <ul>
      <li>根据要求设计逻辑电路</li>
      <li>用原理图或HDL描述输入计算机</li>
      <li>逻辑综合（生成网表、门级优化、工艺映射）</li>
      <li>逻辑功能仿真</li>
      <li>根据特定芯片生成编程数据</li>
      <li>时序仿真（包含延时信息）</li>
      <li>将编程数据写入芯片</li>
    </ul>
    <div class="highlight">
      <strong>💡 FPGA需外部PROM保存编程数据</strong>，每次通电自动装载。<br>
      <strong>CPLD采用E<sup>2</sup>PROM工艺</strong>，断电后逻辑不消失，可在系统编程（ISP特性）。
    </div>
  </div>
'''
    },
    {
        'num': '9', 'file': 'ch09', 'title': '脉冲波形的变换与产生',
        'prev': 'ch08.html', 'prev_label': '← 第8章 FPGA和CPLD',
        'next': 'ch10.html', 'next_label': '第10章 模数与数模转换器 →',
        'tprev': 'ch08.html', 'tprev_label': '← 第8章',
        'tnext': 'ch10.html', 'tnext_label': '第10章 →',
        'content': '''
  <div class="section">
    <h2>📌 教学基本要求</h2>
    <ul>
      <li>正确理解单稳态电路、施密特触发电路、多谐振荡电路的组成及工作原理</li>
      <li>掌握单稳、施密特触发电路、多谐振荡电路的逻辑功能及主要指标计算</li>
      <li>了解555定时器的工作原理</li>
      <li>了解555定时器组成的多谐、单稳、施密特触发电路及外接参数计算</li>
    </ul>
  </div>

  <div class="section">
    <h2>9.1 单稳态电路</h2>
    <div class="def-box">
      <strong>工作特点：</strong><br>
      ① 没有触发信号时处于一种稳定状态。<br>
      ② 在外来触发信号作用下，由稳态翻转到暂稳态。<br>
      ③ 暂稳态的持续时间仅取决于RC参数值，经过一段时间后电路会自动返回到稳态。
    </div>
    <p>输出脉冲宽度：<strong>t<sub>w</sub> ≈ 0.7RC</strong>（由RC充放电时间常数决定）</p>
    <p>集成单稳态触发器74121：输出脉冲宽度 t<sub>w</sub> ≈ 0.7·R<sub>ext</sub>·C<sub>ext</sub></p>
  </div>

  <div class="section">
    <h2>9.2 施密特触发电路</h2>
    <p><strong>特点：</strong></p>
    <ul>
      <li>属于电平触发器件，当输入信号达到某一定电压值时，输出电压会发生突变</li>
      <li>电路有两个阈值电压——<strong>正向阈值电压V<sub>T+</sub></strong>和<strong>负阈值电压V<sub>T-</sub></strong></li>
    </ul>
    <p>应用：波形变换、波形的整形与抗干扰、幅度鉴别。</p>
  </div>

  <div class="section">
    <h2>9.3 多谐振荡电路</h2>
    <p>多谐振荡器不需要外加触发信号就能自动产生矩形脉冲波。</p>
    <p>基本组成：开关器件（产生高、低电平）+ 反馈延迟环节（RC电路的充放电特性实现延时）。</p>
    <p>由门电路组成的多谐振荡电路周期：<strong>T ≈ 2.2RC</strong>。频率稳定性较差。</p>
    <h3>石英晶体多谐振荡电路</h3>
    <p>当f等于串联谐振频率f<sub>s</sub>时，石英晶体呈纯电阻特性，正反馈最强。频率稳定性极高。</p>
  </div>

  <div class="section">
    <h2>9.4 555定时器</h2>
    <p>555定时器是一种应用方便的中规模集成电路，广泛用于信号的产生、变换、控制与检测。详见<a href="chips.html">芯片专题</a>。</p>
    <h3>三种典型应用</h3>
    <ul>
      <li><strong>施密特触发电路</strong>：V<sub>T+</sub> = 2/3V<sub>CC</sub>，V<sub>T-</sub> = 1/3V<sub>CC</sub></li>
      <li><strong>单稳态电路</strong>：t<sub>w</sub> ≈ 1.1RC</li>
      <li><strong>多谐振荡电路</strong>：T ≈ 0.7(R<sub>1</sub> + 2R<sub>2</sub>)C</li>
    </ul>
  </div>
'''
    },
]

def write_page(ch):
    html = PAGE
    # Longer placeholders first to avoid substring conflicts
    for placeholder, value in [
        ('CHAPTER_NUM', ch['num']),
        ('CHAPTER_TITLE', ch['title']),
        ('TOPBAR_PREV_LABEL', ch['tprev_label']),
        ('TOPBAR_NEXT_LABEL', ch['tnext_label']),
        ('TOPBAR_PREV', ch['tprev']),
        ('TOPBAR_NEXT', ch['tnext']),
        ('NAV_PREV_LABEL', ch['prev_label']),
        ('NAV_NEXT_LABEL', ch['next_label']),
        ('NAV_PREV', ch['prev']),
        ('NAV_NEXT', ch['next']),
        ('CONTENT', ch['content']),
    ]:
        html = html.replace(placeholder, value)

    path = os.path.join(os.path.dirname(__file__), ch['file'] + '.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("已生成: " + ch['file'] + '.html')

for ch in CHAPTERS:
    write_page(ch)
