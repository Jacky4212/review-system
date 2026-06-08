"""复习网页生成器 v4 — 修复各项问题"""
import os, json, re

OUT_DIR = r"D:\code\cherry studio\复习\output"
HTML_OUT = r"D:\code\cherry studio\复习\index.html"
EXAM_FILE = os.path.join(OUT_DIR, "考试要点.txt")

# ─── 分组公式 ───
FORMULA_GROUPS = [
    ("放射性衰变", [
        ("衰变定律", "N = N_0 e^{-\\lambda t}"),
        ("衰变常数", "\\lambda = \\frac{\\ln 2}{T_{1/2}}"),
        ("半衰期", "T_{1/2} = \\frac{\\ln 2}{\\lambda}"),
        ("活度定义", "A = \\lambda N = -\\frac{dN}{dt}"),
        ("活度衰变", "A = A_0 e^{-\\lambda t}"),
        ("长期平衡", "\\lambda_1 N_1 = \\lambda_2 N_2"),
    ]),
    ("放射性单位", [
        ("比活度", "S = \\frac{A}{m}"),
        ("居里→贝克换算", "1\\;\\text{Ci} = 3.7 \\times 10^{10}\\;\\text{Bq}"),
    ]),
    ("吸附", [
        ("吸附率", "R = \\frac{C_0 - C}{C_0} \\times 100\\%"),
        ("分配系数", "K_d = \\frac{\\text{固相浓度}}{\\text{液相浓度}}"),
    ]),
    ("溶剂萃取", [
        ("分配比", "D = \\frac{C_{\\text{有}}}{C_{\\text{水}}}"),
        ("分离系数", "\\alpha = \\frac{D_A}{D_B}"),
        ("萃取率", "E = \\frac{D}{D + V_{\\text{水}}/V_{\\text{有}}}}"),
    ]),
    ("电化学", [
        ("能斯特方程", "E = E^0 + \\frac{RT}{nF} \\ln \\frac{a_{\\text{ox}}}{a_{\\text{red}}}"),
    ]),
    ("共沉淀", [
        ("同晶定义", "\\text{类质同晶：晶体结构相同，化学组成类似}"),
        ("分配系数", "D = \\frac{[A]_{\\text{晶}}}{[A]_{\\text{液}}} / \\frac{[B]_{\\text{晶}}}{[B]_{\\text{液}}}"),
    ]),
]

SUBJECTS = {
    "radiochemistry": {
        "name": "放射化学", "nameEn": "Radiochemistry",
        "examDate": "2026-06-18T18:30:00+08:00",
        "examDateLabel": "2026年6月18日",
        "chapters": [
            {"id":"ch1","file":"1.第一章 绪论 (2026)-1(2).txt","title":"第一章 绪论"},
            {"id":"ch2","file":"2.第二章 放射性(2026)-1.txt","title":"第二章 放射性"},
            {"id":"ch3","file":"3.第三章 放射性核素的物理化学.txt","title":"第三章 放射性核素的物理化学"},
            {"id":"ch4","file":"4.第四章 物质的分离.txt","title":"第四章 物质的分离"},
            {"id":"ch5","file":"6. 天然核素-1.txt","title":"第六章 天然放射性元素化学"},
            {"id":"ch6","file":"7. 第七章 锕系理论(2).txt","title":"第七章 锕系理论"},
            {"id":"ch7","file":"8.第八章(2).txt","title":"第八章 裂片元素及活化产物化学"},
            {"id":"ch8","file":"9.第九章 放射性核素的制备.txt","title":"第九章 放射性核素的制备"},
        ],
        "examTopics": [
            {"topic":"学科特点","ch":"ch1","kw":["特点","放射化学","学科","研究","内容"]},
            {"topic":"衰变公式与半衰期","ch":"ch2","kw":["衰变","公式","半衰期","N=","N0","λ","指数","衰变常数"]},
            {"topic":"放射性的单位与比活度","ch":"ch2","kw":["贝克","居里","比活度","Bq","Ci","活度"]},
            {"topic":"衰变类型(α/β/γ)","ch":"ch2","kw":["α衰变","β衰变","γ衰变","衰变类型","α粒子","β粒子"]},
            {"topic":"放射性平衡","ch":"ch2","kw":["平衡","久期平衡","长期平衡","子体","母体"]},
            {"topic":"同位素效应与交换","ch":"ch3","kw":["同位素效应","同位素交换","平衡常数"]},
            {"topic":"放射性胶体","ch":"ch3","kw":["胶体","真胶体","假胶体","分散体系"]},
            {"topic":"吸附作用","ch":"ch3","kw":["吸附","吸附剂","吸附率","吸附系数"]},
            {"topic":"共沉淀与同晶","ch":"ch4","kw":["共沉淀","同晶","同二晶","结晶","混晶"]},
            {"topic":"电化学(能斯特方程)","ch":"ch4","kw":["能斯特","电化学","置换","电沉积","电极"]},
            {"topic":"载体与反载体","ch":"ch4","kw":["载体","反载体","Carrier","放射性核素纯度"]},
            {"topic":"溶剂萃取","ch":"ch4","kw":["萃取","萃取率","萃取剂","盐析剂","掩蔽剂"]},
            {"topic":"离子交换分离","ch":"ch4","kw":["离子交换","稀释液","分离","交换"]},
            {"topic":"天然放射性系","ch":"ch5","kw":["天然放射","放射系","铀系","钍系","母体"]},
            {"topic":"锕系元素与核反应","ch":"ch6","kw":["锕系","核反应","反应式","铀钚","钍铀","转化"]},
            {"topic":"镭氡计算","ch":"ch6","kw":["镭","氡","计算"]},
            {"topic":"核素制备方法","ch":"ch8","kw":["制备","反应堆","加速器","同位素","中子"]},
            {"topic":"同位素稀释法","ch":"ch8","kw":["稀释法","同位素稀释","分析"]},
        ]
    }
}

def load_text(fp):
    path = os.path.join(OUT_DIR, fp)
    if not os.path.exists(path): return [], ""
    with open(path,"r",encoding="utf-8") as f: content = f.read()
    pages = re.split(r'=====\s*第\s*(\d+)\s*页\s*=====', content)
    result = []
    for i in range(1, len(pages), 2):
        n, c = pages[i].strip(), pages[i+1].strip() if i+1<len(pages) else ""
        lines = [l for l in c.split("\n") if l.strip()]
        if lines: result.append({"num":n,"lines":lines})
    return result, (pages[0].strip() if pages else "")

def load_exam():
    if not os.path.exists(EXAM_FILE): return []
    with open(EXAM_FILE,"r",encoding="utf-8") as f: return [l.strip() for l in f if l.strip()]

def flt(lines, kw):
    r = []
    for line in lines:
        s = line.strip()
        if not s or len(s)<3: continue
        if re.match(r'^[\d\s\.,;()\-+*/]+$', s): continue
        if any(k in s for k in kw): r.append(s)
    return r

def ext_topic(topic, pages):
    matched = []
    for p in pages:
        lines = flt(p["lines"], topic["kw"])
        if lines: matched.append({"num":p["num"],"lines":lines[:10]})
    return matched

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build(sid, cfg):
    print(f"  处理: {cfg['name']}")
    exam_lines = load_exam()
    ch_pages = {}
    for ch in cfg["chapters"]: ch_pages[ch["id"]], _ = load_text(ch["file"])

    # ── 考试概览 ──
    ov = ['<div class="ob"><h2>'+cfg["name"]+' 考试概览</h2><div class="date">'+cfg["examDateLabel"]+'</div><div class="og">']
    m = {"填空题":"16分,8题×2分","选择题":"14分,7题含多选","名词解释":"16分,4个×4分","问答题":"24分,4个×6分","计算题":"30分,3题×10分"}
    for line in exam_lines:
        for nm, det in m.items():
            if nm in line and "分" in line:
                sc, dt = det.split(",",1)
                ov.append(f'<div class="oi"><div class="nm">{nm}</div><div class="sc">{sc}</div><div class="dt">{dt}</div></div>')
                break
    ov.append('</div></div>')

    ov.append('<div class="tc"><h3>重点知识</h3><ul>')
    ink = False
    for line in exam_lines:
        if "重点知识" in line: ink=True; continue
        if ink and any(x in line for x in ["注意","铅笔","计算器","AI"]): break
        if ink and line.strip(): ov.append(f'<li>{esc(line)}</li>')
    ov.append('</ul></div>')
    ov.append('<div class="tc"><h3>注意事项</h3><ul>')
    for line in exam_lines:
        if any(x in line for x in ["注意","铅笔","计算器"]): ov.append(f'<li>{esc(line)}</li>')
    ov.append('</ul></div>')
    cfg["ovHTML"] = "\n".join(ov)

    # ── 考点内容（逐页提取，保持上下文）──
    cfg["tpH"] = {}
    for et in cfg["examTopics"]:
        pages = ch_pages.get(et["ch"], [])
        matched = ext_topic(et, pages)
        ch_t = next((c["title"] for c in cfg["chapters"] if c["id"]==et["ch"]), "")
        parts = [f'<div class="th"><h2>{et["topic"]}</h2><div class="src">来源：<a href="#" onclick="nav(\'ch-{et["ch"]}\');return false">{ch_t}</a></div></div>']
        if matched:
            for s in matched:
                parts.append(f'<div class="ts"><div class="sn">第 {s["num"]} 页</div>')
                for line in s["lines"]: parts.append(f'<p>{esc(line)}</p>')
                parts.append('</div>')
        else:
            parts.append(f'<div class="te">参考 <a href="#" onclick="nav(\'ch-{et["ch"]}\');return false">{ch_t}</a></div>')
        cfg["tpH"][et["topic"]] = "\n".join(parts)

    # ── 章节内容（每页完整展示，默认折叠）──
    for ch in cfg["chapters"]:
        pages = ch_pages.get(ch["id"], [])
        if not pages: ch["html"] = ""; continue
        # 找出本本章有哪些考点
        topic_kw = []
        for et in cfg["examTopics"]:
            if et["ch"] == ch["id"]: topic_kw.extend(et["kw"])
        parts = [f'<div class="ch"><h2>{ch["title"]}</h2></div>']
        for p in pages:
            # 检查该页是否有考点内容
            has_exam = any(k in "\n".join(p["lines"]) for k in topic_kw) if topic_kw else False
            expanded = " act" if has_exam else ""
            parts.append(f'<div class="sh"><div class="shd{expanded}" onclick="this.classList.toggle(\'c\');this.nextElementSibling.classList.toggle(\'c\')"><span>第 {p["num"]} 页</span><span class="ic">▼</span></div><div class="sbb c">')
            for line in p["lines"]: parts.append(f'<p>{esc(line)}</p>')
            parts.append('</div></div>')
        ch["html"] = "\n".join(parts)

    # ── 公式（分组）──
    fh = ['<div class="ss"><h3>必背公式</h3>']
    for gname, formulas in FORMULA_GROUPS:
        fh.append(f'<div class="fg"><div class="fg-title">{gname}</div>')
        for nm, tex in formulas:
            fh.append(f'<div class="fi"><div class="fn">{nm}</div><div class="math">`{tex}`</div></div>')
        fh.append('</div>')
    fh.append('</div>')
    cfg["fH"] = "\n".join(fh)

    # ── 名词解释（卡片式：词汇高亮 + 完整原文）──
    seen = set()
    th = ['<div class="ss"><h3>名词解释</h3><div class="tc-grid">']
    for ch in cfg["chapters"]:
        pages = ch_pages.get(ch["id"], [])
        for p in pages:
            for line in p["lines"]:
                s = line.strip()
                if any(k in s for k in ["是指","称为","叫做","指的是"]) and 8<len(s)<120 and s not in seen:
                    seen.add(s)
                    # 提取冒号前的词作为名词
                    term_name = s
                    if "：" in s[:30]:
                        term_name = s.split("：")[0]
                    elif "是指" in s:
                        term_name = s[:s.index("是指")]
                    elif "称为" in s:
                        term_name = s[:s.index("称为")]
                    th.append(f'<div class="tc-card"><span class="tc-term">{esc(term_name)}</span><span class="tc-def">{esc(s)}</span></div>')
    th.append('</div></div>')
    cfg["tH"] = "\n".join(th)
    print(f"  考点 {len(cfg['examTopics'])} 个, 名词 {len(seen)} 个")


HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>复习系统</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>
:root{--bg:#f4f5f7;--surface:#fff;--text:#1a1a2e;--text2:#555;--primary:#4361ee;--plight:#eef0ff;--accent:#e63946;--border:#ddd;--radius:10px;--font:"PingFang SC","Microsoft YaHei",system-ui,sans-serif}
.dark-mode{--bg:#1a1a2e;--surface:#16213e;--text:#e0e0e0;--text2:#889;--primary:#6c8cff;--plight:#1e2a4a;--border:#2a2a4a}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:52px}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}
#progressBar{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--primary),var(--accent));z-index:9999;width:0%;transition:width .08s}
.top{position:sticky;top:0;z-index:100;background:var(--surface);border-bottom:1px solid var(--border);height:48px;padding:0 12px;display:flex;align-items:center;gap:6px}
.top button{background:none;border:none;cursor:pointer;color:var(--primary);padding:4px 6px;border-radius:4px;font-size:1em}
.top button:hover{background:var(--plight)}
.top .ti{flex:1;font-weight:600;font-size:.9em}
.top .ti .en{font-weight:400;color:var(--text2);font-size:.75em;margin-left:4px}
.top .bd{background:var(--accent);color:#fff;padding:2px 10px;border-radius:10px;font-size:.68em}
.top .cd{font-size:.68em;color:var(--text2);white-space:nowrap}
.lo{display:flex;max-width:1400px;margin:0 auto;min-height:calc(100vh - 48px)}
.sb{width:230px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);position:sticky;top:48px;height:calc(100vh - 48px);overflow-y:auto;padding:4px 0}
.sb::-webkit-scrollbar{width:4px}
.sb::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
.sb .st{padding:4px 12px 2px;font-size:.65em;color:var(--text2);font-weight:600}
.sb .it{display:block;padding:4px 12px 4px 16px;color:var(--text);text-decoration:none;font-size:.8em;border-left:3px solid transparent;cursor:pointer;transition:all .1s}
.sb .it:hover{background:var(--plight);color:var(--primary)}
.sb .it.act{background:var(--plight);color:var(--primary);border-left-color:var(--primary);font-weight:600}
.sb .it .n{display:inline-block;width:17px;height:17px;line-height:17px;text-align:center;border-radius:50%;background:var(--bg);font-size:.62em;font-weight:600;margin-right:2px;color:var(--text2)}
.sb .it.act .n{background:var(--primary);color:#fff}
.sb .tp{padding-left:18px;font-size:.78em}
.ma{flex:1;padding:20px 28px 60px;min-width:0}
.bl{display:none;animation:f .2s}
.bl.act{display:block}
@keyframes f{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
.ob{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border-radius:var(--radius);padding:22px 26px;margin-bottom:18px}
.ob h2{font-size:1.2em;margin-bottom:2px}
.ob .date{opacity:.85;font-size:.78em;margin-bottom:12px}
.og{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px}
.oi{background:rgba(255,255,255,.15);border-radius:6px;padding:8px 12px}
.oi .nm{font-size:.75em;opacity:.9}
.oi .sc{font-size:1.2em;font-weight:700}
.oi .dt{font-size:.65em;opacity:.75}
.tc{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;margin-bottom:12px}
.tc h3{color:var(--primary);font-size:.85em;margin-bottom:5px}
.tc ul{padding-left:15px}
.tc li{margin-bottom:2px;color:var(--text2);font-size:.82em}
.th{margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--primary)}
.th h2{font-size:1.15em;color:var(--primary)}
.th .src{font-size:.78em;color:var(--text2);margin-top:2px}
.th .src a{color:var(--primary);text-decoration:none}
.ts{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px 14px;margin-bottom:7px}
.ts .sn{font-size:.7em;color:var(--text2);margin-bottom:3px;font-weight:600}
.ts p{margin-bottom:2px;font-size:.88em}
.sh{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:5px;overflow:hidden}
.shd{padding:5px 12px;background:var(--bg);font-size:.75em;font-weight:600;color:var(--text2);cursor:pointer;user-select:none;display:flex;justify-content:space-between}
.shd:hover{background:var(--plight)}
.shd .ic{transition:transform .2s;font-size:.65em}
.shd.c .ic{transform:rotate(-90deg)}
.sbb{padding:7px 12px;line-height:1.7;font-size:.85em}
.sbb.c{display:none}
.sbb p{margin-bottom:2px}
.ch{margin-bottom:10px}
.ch h2{font-size:1.1em;color:var(--primary);padding-bottom:6px;border-bottom:1px solid var(--border)}
.ss{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;margin-bottom:14px}
.ss h3{font-size:.9em;color:var(--primary);margin-bottom:10px;padding-bottom:4px;border-bottom:1px solid var(--border)}
.fg{margin-bottom:12px}
.fg-title{font-size:.82em;font-weight:600;color:var(--text2);margin-bottom:6px;padding-left:2px}
.fi{background:var(--plight);border-left:3px solid var(--primary);padding:8px 12px;border-radius:6px;margin-bottom:6px}
.fi .fn{font-size:.75em;color:var(--text2);margin-bottom:2px}
.fi .math{font-size:1.05em;padding:2px 0}
/* 名词卡片 */
.tc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:8px}
.tc-card{background:var(--plight);border:1px solid var(--border);border-radius:6px;padding:8px 12px}
.tc-term{display:inline-block;font-weight:600;color:var(--accent);font-size:.85em;margin-bottom:2px;padding:0 4px;border-radius:3px}
.tc-def{display:block;font-size:.82em;color:var(--text);line-height:1.5;margin-top:2px}
.subject-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;max-width:480px;margin:0 auto}
.scd{background:var(--surface);border:2px solid var(--border);border-radius:var(--radius);padding:18px;cursor:pointer;transition:all .2s}
.scd:hover{border-color:var(--primary);transform:translateY(-2px)}
.scd h3{font-size:1em;margin-bottom:2px}
@media(max-width:900px){
.sb{display:none}
.ma{padding:12px}
.og{grid-template-columns:repeat(2,1fr)}
.tc-grid{grid-template-columns:1fr}
}
.mb{display:none;background:none;border:none;font-size:1em;cursor:pointer;color:var(--primary);padding:4px}
@media(max-width:900px){.mb{display:block}}
.so{display:none;position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:200}
.so.s{display:block}
.sb.ms{display:block;position:fixed;left:0;top:0;z-index:300;height:100vh}
@media print{
.top,.sb,#progressBar,.so,.mb{display:none!important}
.lo{display:block}
.ma{padding:0}
.bl{display:block!important;page-break-after:always}
.sh{break-inside:avoid;border:1px solid #ccc}
.sbb{display:block!important}
.shd{background:#f5f5f5;cursor:default}
.shd .ic{display:none}
.ob{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>
</head>
<body>
<div id="progressBar"></div>

<div id="sel" class="bl act" style="max-width:480px;margin:50px auto;padding:0 16px;text-align:center">
  <h1 style="font-size:1.8em;color:var(--primary);margin-bottom:4px;">复习系统</h1>
  <p style="color:var(--text2);margin-bottom:24px;">选择科目</p>
  <div class="subject-cards" id="cards"></div>
</div>

<div id="rev" class="bl">
<div class="top">
  <button onclick="back()">&#8592;</button>
  <button class="mb" onclick="ts()">&#9776;</button>
  <div class="ti"><span id="st"></span><span class="en" id="se"></span></div>
  <span class="bd" id="sb"></span>
  <span class="cd" id="sc"></span>
  <button onclick="td()" id="dtBtn">🌙</button>
</div>
<div class="so" onclick="ts()" id="so"></div>
<div class="lo">
  <nav class="sb" id="sidebar"></nav>
  <main class="ma" id="main"></main>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script>
const D = %DATA%;
let C = null;

function back(){document.getElementById('sel').classList.add('act');document.getElementById('rev').classList.remove('act');document.title='复习系统';}

function enter(id){
  C=D[id];
  document.getElementById('sel').classList.remove('act');
  document.getElementById('rev').classList.add('act');
  document.getElementById('st').textContent=C.name;
  document.getElementById('se').textContent=C.nameEn;
  document.getElementById('sb').textContent=C.examDateLabel;
  ud(); rs(); rm();
  setTimeout(function(){document.querySelectorAll('.math').forEach(function(el){try{katex.render(el.textContent.slice(1,-1),el,{displayMode:false})}catch(e){console.log(e)}})},100);
  nav('overview');
}

function rs(){
  var s=document.getElementById('sidebar');
  var h='<div class="st">概览</div><a class="it act" data-t="overview" onclick="nav(\'overview\')">考试概览</a>';
  h+='<div class="st">考点复习</div>';
  C.examTopics.forEach(function(t,i){h+='<a class="it tp" data-t="topic-'+i+'" onclick="nav(\'topic-'+i+'\')">'+t.topic+'</a>';});
  h+='<div class="st">章节浏览</div>';
  C.chapters.forEach(function(c,i){h+='<a class="it" data-t="ch-'+c.id+'" onclick="nav(\'ch-'+c.id+'\')"><span class="n">'+(i+1)+'</span>'+c.title+'</a>';});
  h+='<div class="st">专题</div><a class="it" data-t="formulas" onclick="nav(\'formulas\')">公式</a><a class="it" data-t="terms" onclick="nav(\'terms\')">名词解释</a>';
  s.innerHTML=h;
}

function rm(){
  var m=document.getElementById('main');
  var h='<div id="s-overview" class="bl act">'+C.ovHTML+'</div>';
  C.examTopics.forEach(function(t,i){h+='<div id="s-topic-'+i+'" class="bl">'+(C.tpH[t.topic]||'')+'</div>';});
  C.chapters.forEach(function(c){h+='<div id="s-ch-'+c.id+'" class="bl">'+(c.html||'')+'</div>';});
  h+='<div id="s-formulas" class="bl">'+C.fH+'</div>';
  h+='<div id="s-terms" class="bl">'+C.tH+'</div>';
  m.innerHTML=h;
}

function nav(t){
  document.querySelectorAll('.sb .it').forEach(function(e){e.classList.remove('act');});
  var si=document.querySelector('.sb .it[data-t="'+t+'"]');if(si)si.classList.add('act');
  document.querySelectorAll('.ma .bl').forEach(function(e){e.classList.remove('act');});
  var sec=document.getElementById('s-'+t);if(sec){sec.classList.add('act');sec.scrollIntoView({behavior:'smooth',block:'start'});}
}

function ts(){document.getElementById('sidebar').classList.toggle('ms');document.getElementById('so').classList.toggle('s');}

function td(){
  document.body.classList.toggle('dark-mode');
  var b=document.getElementById('dtBtn');
  b.textContent=document.body.classList.contains('dark-mode')?'☀️':'🌙';
  localStorage.setItem('rd',document.body.classList.contains('dark-mode')?'1':'0');
}
if(localStorage.getItem('rd')==='1'){document.body.classList.add('dark-mode');document.getElementById('dtBtn').textContent='☀️';}

function ud(){var e=document.getElementById('sc');if(!e||!C)return;var d=new Date(C.examDate).getTime()-Date.now();if(d<=0){e.textContent='考试已开始';return;}e.textContent=Math.floor(d/86400000)+'天'+Math.floor((d%86400000)/3600000)+'小时';}
setInterval(ud,60000);

window.addEventListener('scroll',function(){var b=document.getElementById('progressBar');if(!b)return;var s=window.scrollY,d=document.documentElement.scrollHeight-window.innerHeight;if(d>0)b.style.width=(s/d*100)+'%';});

(function(){var c=document.getElementById('cards');var h='';for(var[id,sub]of Object.entries(D)){h+='<div class="scd" onclick="enter(\''+id+'\')"><h3>'+sub.name+'</h3><div style="font-size:.78em;color:var(--text2)">'+sub.nameEn+'</div><div style="margin-top:4px;font-size:.75em;color:var(--text2)">'+sub.examTopics.length+' 考点</div></div>';}c.innerHTML=h;var k=Object.keys(D);if(k.length===1)enter(k[0]);})();
</script>
</body>
</html>'''

def main():
    print("="*40)
    print("复习网页生成器 v4")
    print("="*40)
    for sid, cfg in SUBJECTS.items(): build(sid, cfg)
    h = HTML.replace("%DATA%", json.dumps(SUBJECTS, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8") as f: f.write(h)
    print(f"\n生成: {HTML_OUT} ({os.path.getsize(HTML_OUT)/1024:.0f} KB)")

if __name__ == "__main__":
    main()
