"""
复习网页生成器 v2
以考点为主线组织内容，按需展示PPT中最相关的部分
"""

import os, json, re

OUT_DIR = r"D:\code\cherry studio\复习\output"
HTML_OUT = r"D:\code\cherry studio\复习\index.html"
EXAM_FILE = os.path.join(OUT_DIR, "考试要点.txt")

# ─── 科目配置 ───
SUBJECTS = {
    "radiochemistry": {
        "name": "放射化学", "nameEn": "Radiochemistry",
        "examDate": "2026-06-18T18:30:00+08:00",
        "examDateLabel": "2026年6月18日",
        "chapters": [
            {"id": "ch1", "file": "1.第一章 绪论 (2026)-1(2).txt",  "title": "第一章 绪论"},
            {"id": "ch2", "file": "2.第二章 放射性(2026)-1.txt",    "title": "第二章 放射性"},
            {"id": "ch3", "file": "3.第三章 放射性核素的物理化学.txt", "title": "第三章 放射性核素的物理化学"},
            {"id": "ch4", "file": "4.第四章 物质的分离.txt",         "title": "第四章 物质的分离"},
            {"id": "ch5", "file": "6. 天然核素-1.txt",               "title": "第六章 天然放射性元素化学"},
            {"id": "ch6", "file": "7. 第七章 锕系理论(2).txt",       "title": "第七章 锕系理论"},
            {"id": "ch7", "file": "8.第八章(2).txt",                 "title": "第八章 裂片元素及活化产物化学"},
            {"id": "ch8", "file": "9.第九章 放射性核素的制备.txt",   "title": "第九章 放射性核素的制备"},
        ],
        "examTopics": [
            {"topic": "学科特点",  "ch": "ch1", "keywords": ["特点", "放射化学", "学科", "研究", "内容"]},
            {"topic": "衰变公式与半衰期", "ch": "ch2", "keywords": ["衰变", "公式", "半衰期", "N=", "N0", "λ", "指数", "衰变常数"]},
            {"topic": "放射性的单位与比活度", "ch": "ch2", "keywords": ["贝克", "居里", "比活度", "Bq", "Ci", "活度"]},
            {"topic": "衰变类型(α/β/γ)", "ch": "ch2", "keywords": ["α衰变", "β衰变", "γ衰变", "衰变类型", "α粒子", "β粒子"]},
            {"topic": "放射性平衡", "ch": "ch2", "keywords": ["平衡", "久期平衡", "长期平衡", "子体", "母体"]},
            {"topic": "同位素效应与交换", "ch": "ch3", "keywords": ["同位素效应", "同位素交换", "平衡常数"]},
            {"topic": "放射性胶体", "ch": "ch3", "keywords": ["胶体", "真胶体", "假胶体", "分散体系"]},
            {"topic": "吸附作用", "ch": "ch3", "keywords": ["吸附", "吸附剂", "吸附率", "吸附系数"]},
            {"topic": "共沉淀与同晶", "ch": "ch4", "keywords": ["共沉淀", "同晶", "同二晶", "结晶", "混晶"]},
            {"topic": "电化学(能斯特方程)", "ch": "ch4", "keywords": ["能斯特", "电化学", "置换", "电沉积", "电极"]},
            {"topic": "载体与反载体", "ch": "ch4", "keywords": ["载体", "反载体", "Carrier", "放射性核素纯度"]},
            {"topic": "溶剂萃取", "ch": "ch4", "keywords": ["萃取", "萃取率", "萃取剂", "盐析剂", "掩蔽剂"]},
            {"topic": "离子交换分离", "ch": "ch4", "keywords": ["离子交换", "稀释液", "分离", "交换"]},
            {"topic": "天然放射性系", "ch": "ch5", "keywords": ["天然放射", "放射系", "铀系", "钍系", "母体"]},
            {"topic": "锕系元素与核反应", "ch": "ch6", "keywords": ["锕系", "核反应", "反应式", "铀钚", "钍铀", "转化"]},
            {"topic": "镭氡计算", "ch": "ch6", "keywords": ["镭", "氡", "计算"]},
            {"topic": "核素制备方法", "ch": "ch8", "keywords": ["制备", "反应堆", "加速器", "同位素", "中子"]},
            {"topic": "同位素稀释法", "ch": "ch8", "keywords": ["稀释法", "同位素稀释", "分析"]},
        ]
    }
}


def load_text(filepath):
    path = os.path.join(OUT_DIR, filepath)
    if not os.path.exists(path):
        return [], f"文件未找到: {filepath}"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pages = re.split(r'=====\s*第\s*(\d+)\s*页\s*=====', content)
    result = []
    for i in range(1, len(pages), 2):
        page_num = pages[i].strip()
        page_content = pages[i + 1].strip() if i + 1 < len(pages) else ""
        lines = [l for l in page_content.split("\n") if l.strip()]
        if lines:
            result.append({"num": page_num, "lines": lines})
    return result, (pages[0].strip() if pages else "")


def load_exam_lines():
    if not os.path.exists(EXAM_FILE):
        return []
    with open(EXAM_FILE, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def filter_relevant(lines, keywords):
    relevant = []
    for line in lines:
        s = line.strip()
        if not s or len(s) < 3:
            continue
        if re.match(r'^[\d\s\.\,\;\(\)\-\+\*/]+$', s):
            continue
        if any(kw in s for kw in keywords):
            relevant.append(s)
    return relevant


def extract_topic(topic, pages):
    kw = topic["keywords"]
    matched = []
    for p in pages:
        lines = filter_relevant(p["lines"], kw)
        if lines:
            matched.append({"num": p["num"], "lines": lines[:8]})
    return matched


def build_subject(sid, cfg):
    print(f"  处理: {cfg['name']}")

    exam_lines = load_exam_lines()

    # load all chapters
    ch_pages = {}
    for ch in cfg["chapters"]:
        ch_pages[ch["id"]], _ = load_text(ch["file"])

    # --- exam overview ---
    ov = []
    ov.append('<div class="overview-banner">')
    ov.append(f'<h2>{cfg["name"]} 考试概览</h2>')
    ov.append(f'<div class="date">考试时间：{cfg["examDateLabel"]}</div>')

    type_map = {
        "填空题": ("16分", "8题 x 2分"), "选择题": ("14分", "7题，含多选"),
        "名词解释": ("16分", "4个 x 4分"), "问答题": ("24分", "4个 x 6分"),
        "计算题": ("30分", "3题 x 10分")
    }
    ov.append('<div class="overview-grid">')
    for line in exam_lines:
        for name, (score, detail) in type_map.items():
            if name in line and "分" in line:
                ov.append(f'<div class="overview-item"><div class="name">{name}</div><div class="score">{score}</div><div class="detail">{detail}</div></div>')
                break
    ov.append('</div></div>')

    ov.append('<div class="tips-card"><h3>重点知识</h3><ul>')
    in_kw = False
    for line in exam_lines:
        if "重点知识" in line:
            in_kw = True
            continue
        if in_kw and any(x in line for x in ["注意", "铅笔", "计算器", "AI"]):
            break
        if in_kw and line.strip():
            ov.append(f'<li>{line.strip()}</li>')
    ov.append('</ul></div>')

    ov.append('<div class="tips-card"><h3>注意事项</h3><ul>')
    for line in exam_lines:
        if any(x in line for x in ["注意", "铅笔", "计算器"]):
            ov.append(f'<li>{line.strip()}</li>')
    ov.append('</ul></div>')

    cfg["examOverviewHTML"] = "\n".join(ov)

    # --- topic content ---
    cfg["topicsHTML"] = {}
    for et in cfg["examTopics"]:
        pages = ch_pages.get(et["ch"], [])
        matched = extract_topic(et, pages)
        ch_title = next((c["title"] for c in cfg["chapters"] if c["id"] == et["ch"]), "")

        parts = []
        parts.append(f'<div class="topic-header"><h2>{et["topic"]}</h2><div class="topic-source">来源：<a href="#" onclick="navigate(\'ch-{et["ch"]}\');return false">{ch_title}</a></div></div>')
        if matched:
            for slide in matched:
                parts.append('<div class="topic-slide">')
                parts.append(f'<div class="topic-slide-num">第 {slide["num"]} 页</div>')
                for line in slide["lines"]:
                    e = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                    if any(c in line for c in ["=","λ","×","ln","lg"]) and any(c.isdigit() for c in line) and len(line) < 100:
                        parts.append(f'<div class="topic-formula">{e}</div>')
                    else:
                        parts.append(f'<p>{e}</p>')
                parts.append('</div>')
        else:
            parts.append(f'<div class="topic-empty">参考 <a href="#" onclick="navigate(\'ch-{et["ch"]}\');return false">{ch_title}</a> 相关内容</div>')
        cfg["topicsHTML"][et["topic"]] = "\n".join(parts)

    # --- chapter content ---
    for ch in cfg["chapters"]:
        pages = ch_pages.get(ch["id"], [])
        if not pages:
            ch["html"] = '<div class="empty-state"><p>内容加载中...</p></div>'
            continue
        parts = [f'<div class="chapter-header"><h2>{ch["title"]}</h2></div>']
        for p in pages:
            parts.append('<div class="slide-card">')
            parts.append(f'<div class="slide-header" onclick="this.classList.toggle(\'collapsed\');this.nextElementSibling.classList.toggle(\'collapsed\')"><span>第 {p["num"]} 页</span><span class="icon">▼</span></div>')
            parts.append('<div class="slide-body collapsed">')
            for line in p["lines"]:
                e = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                parts.append(f'<p>{e}</p>')
            parts.append('</div></div>')
        ch["html"] = "\n".join(parts)

    # --- formulas ---
    formulas = set()
    for et in cfg["examTopics"]:
        pages = ch_pages.get(et["ch"], [])
        matched = extract_topic(et, pages)
        for slide in matched:
            for line in slide["lines"]:
                if any(c in line for c in ["=","λ","×","ln","lg"]) and any(c.isdigit() for c in line) and 4 < len(line) < 120:
                    zh = sum(1 for c in line if 'u4e00' <= c <= 'u9fff')
                    if zh / max(len(line), 1) < 0.5:
                        formulas.add(line.strip())
    fh = ['<div class="special-section"><h3>必背公式</h3><div class="formula-grid">']
    for f in sorted(formulas):
        e = f.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        fh.append(f'<div class="formula-item">{e}</div>')
    fh.append('</div></div>')
    cfg["formulasHTML"] = "\n".join(fh)

    # --- terms ---
    seen = set()
    th = ['<div class="special-section"><h3>名词解释</h3><ul class="term-list">']
    for ch in cfg["chapters"]:
        pages = ch_pages.get(ch["id"], [])
        for p in pages:
            for line in p["lines"]:
                s = line.strip()
                if any(k in s for k in ["是指","称为","叫做","指的是"]) and 8 < len(s) < 100 and s not in seen:
                    seen.add(s)
                    e = s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                    th.append(f'<li>{e}</li>')
    th.append('</ul></div>')
    cfg["termsHTML"] = "\n".join(th)

    print(f"  考点 {len(cfg['examTopics'])} 个, 公式 {len(formulas)} 条, 名词 {len(seen)} 个")


TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>复习系统</title>
<style>
:root{--bg:#f4f5f7;--surface:#fff;--text:#1a1a2e;--text2:#666;--primary:#4361ee;--primary-light:#eef0ff;--accent:#e63946;--border:#ddd;--radius:10px;--shadow:0 1px 6px rgba(0,0,0,0.06);--font:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;--mono:"Cascadia Code",Consolas,monospace}
.dark-mode{--bg:#1a1a2e;--surface:#16213e;--text:#e0e0e0;--text2:#889;--primary:#6c8cff;--primary-light:#1e2a4a;--border:#2a2a4a;--shadow:0 1px 6px rgba(0,0,0,0.3)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:56px}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}

#progressBar{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--primary),var(--accent));z-index:9999;width:0%;transition:width .1s}

/* topbar */
.topbar{position:sticky;top:0;z-index:100;background:var(--surface);border-bottom:1px solid var(--border);height:48px;padding:0 12px;display:flex;align-items:center;gap:6px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}
.topbar button{background:none;border:none;cursor:pointer;color:var(--primary);padding:4px 6px;border-radius:4px;font-size:1em}
.topbar button:hover{background:var(--primary-light)}
.topbar .title{flex:1;font-weight:600;font-size:.9em}
.topbar .title .en{font-weight:400;color:var(--text2);font-size:.78em;margin-left:4px}
.topbar .badge{background:var(--accent);color:#fff;padding:2px 10px;border-radius:10px;font-size:.7em}
.topbar .cd{font-size:.7em;color:var(--text2)}
#searchBox{padding:3px 10px;border:1px solid var(--border);border-radius:12px;font-size:.8em;font-family:var(--font);outline:none;width:120px;background:var(--bg);color:var(--text);display:none}

/* layout */
.layout{display:flex;max-width:1400px;margin:0 auto;min-height:calc(100vh - 48px)}

/* sidebar */
.sidebar{width:240px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);position:sticky;top:48px;height:calc(100vh - 48px);overflow-y:auto;padding:6px 0}
.sidebar::-webkit-scrollbar{width:4px}
.sidebar::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
.sidebar .st{padding:5px 14px 3px;font-size:.68em;text-transform:uppercase;letter-spacing:.06em;color:var(--text2);font-weight:600}
.sidebar .it{display:block;padding:5px 14px 5px 18px;color:var(--text);text-decoration:none;font-size:.82em;border-left:3px solid transparent;cursor:pointer;transition:all .1s}
.sidebar .it:hover{background:var(--primary-light);color:var(--primary)}
.sidebar .it.active{background:var(--primary-light);color:var(--primary);border-left-color:var(--primary);font-weight:600}
.sidebar .it .num{display:inline-block;width:18px;height:18px;line-height:18px;text-align:center;border-radius:50%;background:var(--bg);font-size:.65em;font-weight:600;margin-right:3px;color:var(--text2)}
.sidebar .it.active .num{background:var(--primary);color:#fff}
.sidebar .ti{padding-left:20px;font-size:.8em}

/* main */
.main{flex:1;padding:20px 28px 60px;min-width:0}
.block{display:none;animation:f .25s}
.block.active{display:block}
@keyframes f{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

/* overview */
.ob{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border-radius:var(--radius);padding:24px 28px;margin-bottom:20px}
.ob h2{font-size:1.3em;margin-bottom:4px}
.ob .date{opacity:.85;font-size:.82em;margin-bottom:14px}
.og{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px}
.oi{background:rgba(255,255,255,.15);border-radius:6px;padding:8px 12px}
.oi .nm{font-size:.78em;opacity:.9}
.oi .sc{font-size:1.3em;font-weight:700}
.oi .dt{font-size:.68em;opacity:.75}
.tc{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;margin-bottom:14px}
.tc h3{color:var(--primary);font-size:.9em;margin-bottom:6px}
.tc ul{padding-left:16px}
.tc li{margin-bottom:2px;color:var(--text2);font-size:.85em}

/* topic */
.th{margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--primary)}
.th h2{font-size:1.2em;color:var(--primary)}
.th .src{font-size:.8em;color:var(--text2);margin-top:3px}
.th .src a{color:var(--primary);text-decoration:none}
.ts{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;margin-bottom:8px;box-shadow:var(--shadow)}
.ts .sn{font-size:.72em;color:var(--text2);margin-bottom:4px;font-weight:600}
.ts p{margin-bottom:2px;font-size:.9em}
.tf{font-family:var(--mono);background:var(--primary-light);padding:4px 10px;border-radius:4px;margin:3px 0;border-left:3px solid var(--primary);font-size:.85em}
.te{color:var(--text2);font-size:.85em;padding:16px 0}
.te a{color:var(--primary);text-decoration:none}

/* chapter */
.sh{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:6px;overflow:hidden}
.shd{padding:6px 14px;background:var(--bg);font-size:.78em;font-weight:600;color:var(--text2);cursor:pointer;user-select:none;display:flex;justify-content:space-between}
.shd:hover{background:var(--primary-light)}
.shd .ic{transition:transform .2s;font-size:.7em}
.shd.c .ic{transform:rotate(-90deg)}
.sb{padding:8px 14px;line-height:1.8;font-size:.88em}
.sb.c{display:none}
.sb p{margin-bottom:3px}

/* special */
.ss{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;margin-bottom:16px}
.ss h3{font-size:.95em;color:var(--primary);margin-bottom:10px;padding-bottom:4px;border-bottom:1px solid var(--border)}
.fg{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px}
.fi{background:var(--primary-light);border-left:3px solid var(--primary);padding:6px 10px;border-radius:4px;font-family:var(--mono);font-size:.82em}
.tl{padding-left:16px}
.tl li{margin-bottom:4px;font-size:.85em;color:var(--text2)}

/* subject cards */
.sc{max-width:500px;margin:40px auto;padding:0 16px}
.sc h1{text-align:center;font-size:1.8em;color:var(--primary);margin-bottom:4px}
.sc p{text-align:center;color:var(--text2);margin-bottom:28px;font-size:.9em}
.scc{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
.sccd{background:var(--surface);border:2px solid var(--border);border-radius:var(--radius);padding:20px;cursor:pointer;transition:all .2s;box-shadow:var(--shadow)}
.sccd:hover{border-color:var(--primary);transform:translateY(-2px)}
.sccd h3{font-size:1.05em;margin-bottom:2px}

/* mobile */
@media(max-width:900px){
.sidebar{display:none}
.main{padding:12px}
.og{grid-template-columns:repeat(2,1fr)}
.fg{grid-template-columns:1fr}
}
.so{display:none;position:fixed;inset:0;background:rgba(0,0,0,.3);z-index:200}
.so.s{display:block}
.sidebar.ms{display:block;position:fixed;left:0;top:0;z-index:300;height:100vh;box-shadow:4px 0 20px rgba(0,0,0,.15)}
.mb{display:none;background:none;border:none;font-size:1em;cursor:pointer;color:var(--primary);padding:4px}
@media(max-width:900px){.mb{display:block}}

@media print{
.topbar,.sidebar,.mb,.so,#progressBar,#searchBox{display:none!important}
.layout{display:block}
.main{padding:0}
.block{display:block!important;page-break-after:always}
.sh{break-inside:avoid;border:1px solid #ccc}
.sb{display:block!important}
.shd{background:#f5f5f5;cursor:default}
.shd .ic{display:none}
.ob{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>
</head>
<body>
<div id="progressBar"></div>

<div id="subjectSelector" class="block active" style="max-width:500px;margin:40px auto;padding:0 16px;">
  <h1 style="text-align:center;font-size:1.8em;color:var(--primary);margin-bottom:4px;">复习系统</h1>
  <p style="text-align:center;color:var(--text2);margin-bottom:28px;">选择科目开始复习</p>
  <div id="subjectCards" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;"></div>
</div>

<div id="reviewPage" class="block">
  <div class="topbar">
    <button onclick="backHome()">&larr;</button>
    <button class="mb" onclick="toggleS()">&#9776;</button>
    <div class="title"><span id="stitle"></span><span class="en" id="sen"></span></div>
    <span class="badge" id="sbadge"></span>
    <span class="cd" id="scd"></span>
    <button onclick="toggleDark()" id="dtb" style="font-size:.9em;">&#127769;</button>
    <input type="text" id="searchBox" placeholder="搜索...">
  </div>
  <div id="sidebarOverlay" class="so" onclick="toggleS()"></div>
  <div class="layout">
    <nav class="sidebar" id="sidebar"></nav>
    <main class="main" id="mainContent"></main>
  </div>
</div>

<script>
const DATA = %DATA%;
let C = null;

function backHome(){
  document.getElementById('subjectSelector').classList.add('active');
  document.getElementById('reviewPage').classList.remove('active');
  document.getElementById('searchBox').style.display='none';
  document.title='复习系统';
}

function enterSubject(id){
  C=DATA[id];
  document.getElementById('subjectSelector').classList.remove('active');
  document.getElementById('reviewPage').classList.add('active');
  document.getElementById('stitle').textContent=C.name;
  document.getElementById('sen').textContent=C.nameEn;
  document.getElementById('sbadge').textContent=C.examDateLabel;
  document.getElementById('searchBox').style.display='';
  document.getElementById('searchBox').value='';
  updateCD();
  renderS();
  renderM();
  nav('overview');
}

function renderS(){
  const sb=document.getElementById('sidebar');
  let h='<div class="st">概览</div><a class="it active" data-t="overview" onclick="nav(\'overview\')">考试概览</a>';
  h+='<div class="st">考点复习</div>';
  C.examTopics.forEach((t,i)=>{
    h+='<a class="it ti" data-t="topic-'+i+'" onclick="nav(\'topic-'+i+'\')">'+t.topic+'</a>';
  });
  h+='<div class="st">章节浏览</div>';
  C.chapters.forEach((c,i)=>{
    h+='<a class="it" data-t="ch-'+c.id+'" onclick="nav(\'ch-'+c.id+'\')"><span class="num">'+(i+1)+'</span>'+c.title+'</a>';
  });
  h+='<div class="st">专题</div><a class="it" data-t="formulas" onclick="nav(\'formulas\')">公式</a><a class="it" data-t="terms" onclick="nav(\'terms\')">名词解释</a>';
  sb.innerHTML=h;
}

function renderM(){
  const mc=document.getElementById('mainContent');
  let h='<div id="section-overview" class="block active">'+C.examOverviewHTML+'</div>';
  C.examTopics.forEach((t,i)=>{
    h+='<div id="section-topic-'+i+'" class="block">'+(C.topicsHTML[t.topic]||'')+'</div>';
  });
  C.chapters.forEach(c=>{
    h+='<div id="section-ch-'+c.id+'" class="block">'+(c.html||'')+'</div>';
  });
  h+='<div id="section-formulas" class="block">'+C.formulasHTML+'</div>';
  h+='<div id="section-terms" class="block">'+C.termsHTML+'</div>';
  mc.innerHTML=h;
}

function nav(t){
  document.querySelectorAll('.sidebar .it').forEach(e=>e.classList.remove('active'));
  const si=document.querySelector('.sidebar .it[data-t="'+t+'"]');
  if(si) si.classList.add('active');
  document.querySelectorAll('.main .block').forEach(e=>e.classList.remove('active'));
  const sec=document.getElementById('section-'+t);
  if(sec){sec.classList.add('active');sec.scrollIntoView({behavior:'smooth',block:'start'});}
}

function toggleS(){
  document.getElementById('sidebar').classList.toggle('ms');
  document.getElementById('sidebarOverlay').classList.toggle('s');
}

document.getElementById('searchBox').addEventListener('input',function(){
  const q=this.value.toLowerCase().trim();
  document.querySelectorAll('.sh').forEach(c=>{
    const b=c.querySelector('.sb');
    if(!q||(b&&b.textContent.toLowerCase().includes(q))){c.style.display='';if(b)b.classList.remove('c');c.querySelector('.shd')?.classList.remove('c');}
    else c.style.display='none';
  });
});

function toggleDark(){
  document.body.classList.toggle('dark-mode');
  const b=document.getElementById('dtb');
  b.textContent=document.body.classList.contains('dark-mode')?'&#9728;':'&#127769;';
  localStorage.setItem('rd',document.body.classList.contains('dark-mode')?'1':'0');
}
if(localStorage.getItem('rd')==='1'){document.body.classList.add('dark-mode');document.getElementById('dtb').textContent='&#9728;';}

function updateCD(){
  const el=document.getElementById('scd');
  if(!el||!C)return;
  const d=new Date(C.examDate).getTime()-Date.now();
  if(d<=0){el.textContent='考试已开始';return;}
  const dd=Math.floor(d/86400000),hh=Math.floor((d%86400000)/3600000);
  el.textContent=dd+'天'+hh+'小时';
}
setInterval(updateCD,60000);

window.addEventListener('scroll',function(){
  const bar=document.getElementById('progressBar');
  if(!bar)return;
  const st=window.scrollY,dh=document.documentElement.scrollHeight-window.innerHeight;
  if(dh>0)bar.style.width=(st/dh*100)+'%';
});

(function(){
  const c=document.getElementById('subjectCards');
  let h='';
  for(const[id,sub]of Object.entries(DATA)){
    h+='<div class="sccd" onclick="enterSubject(\''+id+'\')"><h3>'+sub.name+'</h3><div style="font-size:.8em;color:var(--text2)">'+sub.nameEn+'</div><div style="margin-top:6px;font-size:.78em;color:var(--text2)">'+sub.examTopics.length+' 考点</div></div>';
  }
  c.innerHTML=h;
  const k=Object.keys(DATA);
  if(k.length===1)enterSubject(k[0]);
})();
</script>
</body>
</html>'''

def main():
    print("=" * 40)
    print("复习网页生成器 v2")
    print("=" * 40)
    for sid, cfg in SUBJECTS.items():
        build_subject(sid, cfg)
    html = TEMPLATE.replace("%DATA%", json.dumps(SUBJECTS, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)
    size = os.path.getsize(HTML_OUT) / 1024
    print(f"\n生成: {HTML_OUT} ({size:.0f} KB)")
    print(f"科目: {len(SUBJECTS)}, 考点: {sum(len(s['examTopics']) for s in SUBJECTS.values())}")

if __name__ == "__main__":
    main()
