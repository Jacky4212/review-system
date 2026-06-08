"""复习网页生成器 v5 — 上下标处理 + 考点题型标签 + 删章节浏览"""
import os, json, re

OUT_DIR = r"D:\code\cherry studio\复习\output"
HTML_OUT = r"D:\code\cherry studio\复习\index.html"
EXAM_FILE = os.path.join(OUT_DIR, "考试要点.txt")

# ─── 考点→题型映射 ───
TOPIC_TYPES = {
    "学科特点":"填空","衰变公式与半衰期":"计算","放射性的单位与比活度":"计算",
    "衰变类型(α/β/γ)":"选择","放射性平衡":"选择/填空","同位素效应与交换":"选择/填空",
    "放射性胶体":"填空/选择","吸附作用":"填空/计算","共沉淀与同晶":"填空/选择",
    "电化学(能斯特方程)":"计算/选择","载体与反载体":"问答","溶剂萃取":"问答/填空",
    "离子交换分离":"问答/填空","天然放射性系":"选择/填空","锕系元素与核反应":"问答/计算",
    "镭氡计算":"计算","核素制备方法":"填空/问答","同位素稀释法":"填空/计算",
}
TYPE_COLORS = {"填空":"#4361ee","选择":"#06d6a0","计算":"#e63946","问答":"#f77f00","填空/选择":"#4361ee","选择/填空":"#06d6a0","填空/计算":"#4361ee","计算/选择":"#e63946","问答/填空":"#f77f00","问答/计算":"#f77f00","选择/填空":"#06d6a0","填空/问答":"#4361ee"}

FORMULA_GROUPS = [
    ("放射性衰变", [
        ("衰变定律","N = N_0 e^{-\\lambda t}"),
        ("衰变定律(另一形式)","N = N_0 \\left(\\frac{1}{2}\\right)^{t/T_{1/2}}"),
        ("时间计算","t = \\frac{1}{\\lambda} \\ln \\frac{N_0}{N}"),
        ("衰变常数","\\lambda = \\frac{\\ln 2}{T_{1/2}}"),
        ("半衰期","T_{1/2} = \\frac{\\ln 2}{\\lambda}"),
        ("活度定义","A = \\lambda N = -\\frac{dN}{dt}"),
        ("初始活度","A_0 = \\lambda N_0"),
        ("活度衰变","A = A_0 e^{-\\lambda t}"),
        ("长期平衡","\\lambda_1 N_1 = \\lambda_2 N_2"),
    ]),
    ("放射性单位", [
        ("比活度","S = \\frac{A}{m}"),
        ("比活度与核素参数","S = \\frac{N_A \\ln 2}{M \\cdot T_{1/2}}"),
        ("居里->贝克换算","1\\;\\text{Ci} = 3.7 \\times 10^{10}\\;\\text{Bq}"),
    ]),
    ("吸附", [
        ("吸附率","R = \\frac{C_0 - C}{C_0} \\times 100\\%"),
        ("吸附量","q = \\frac{V(C_0 - C)}{m}"),
        ("分配系数","K_d = \\frac{\\text{固相浓度}}{\\text{液相浓度}}"),
    ]),
    ("溶剂萃取", [
        ("分配比","D = \\frac{C_{\\text{有}}}{C_{\\text{水}}}"),
        ("分离系数","\\alpha = \\frac{D_A}{D_B}"),
        ("萃取率(一次)","E = \\frac{D}{D + V_{\\text{水}}/V_{\\text{有}}}}"),
        ("萃取率(多次)","E_n = 1 - \\left(\\frac{1}{D+1}\\right)^n"),
    ]),
    ("电化学", [
        ("能斯特方程","E = E^0 + \\frac{RT}{nF} \\ln \\frac{a_{\\text{ox}}}{a_{\\text{red}}}"),
    ]),
    ("共沉淀", [
        ("同晶定义","\\text{类质同晶：晶体结构相同，化学组成类似}"),
        ("分配系数","D = \\frac{[A]_{\\text{晶}}}{[A]_{\\text{液}}} / \\frac{[B]_{\\text{晶}}}{[B]_{\\text{液}}}"),
    ]),
]

SUBJECTS = {
    "radiochemistry": {
        "name":"放射化学","nameEn":"Radiochemistry",
        "examDate":"2026-06-18T18:30:00+08:00","examDateLabel":"2026年6月18日",
        "chapters":[
            {"id":"ch1","file":"1.第一章 绪论 (2026)-1(2).txt","title":"第一章 绪论"},
            {"id":"ch2","file":"2.第二章 放射性(2026)-1.txt","title":"第二章 放射性"},
            {"id":"ch3","file":"3.第三章 放射性核素的物理化学.txt","title":"第三章 放射性核素的物理化学"},
            {"id":"ch4","file":"4.第四章 物质的分离.txt","title":"第四章 物质的分离"},
            {"id":"ch5","file":"6. 天然核素-1.txt","title":"第六章 天然放射性元素化学"},
            {"id":"ch6","file":"7. 第七章 锕系理论(2).txt","title":"第七章 锕系理论"},
            {"id":"ch7","file":"8.第八章(2).txt","title":"第八章 裂片元素及活化产物化学"},
            {"id":"ch8","file":"9.第九章 放射性核素的制备.txt","title":"第九章 放射性核素的制备"},
        ],
        "examTopics":[
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

# ─── 上下标格式化 ───
def fmt_sub_super(text):
    """将PPT文本中的上下标格式化为HTML标签"""
    t = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    # 1. 同位素上标: 数字+元素符号(前面不是字母)
    t = re.sub(r'(?<![A-Za-z(])(\d+)([A-Z][a-z]?)(?![a-z])', r'<sup>\1</sup>\2', t)
    # 2. 化学式下标: 元素+数字
    t = re.sub(r'([A-Z][a-z]?)(\d+)', r'\1<sub>\2</sub>', t)
    # 3. 变量下标: 常见变量字母+数字/上标字母
    t = re.sub(r'\b([NnAaTtKkDdMm])(\d+)\b', r'\1<sub>\2</sub>', t)
    # 4. 分数下标: 如T1/2
    t = re.sub(r'([A-Za-z])\(?(\d+)/(\d+)\)?', r'\1<sub>\2/\3</sub>', t)
    # 5. 指数: e-后面跟字母/数字
    t = re.sub(r'\be-([λ\dμρσ]+[A-Za-z]*)', r'e<sup>-\1</sup>', t)
    # 6. 单位中的-1,-2等上标(如cm-1, s-1)
    t = re.sub(r'([A-Za-z]+)(\(-?\d+\))', r'\1<sup>\2</sup>', t)
    return t

def load_text(fp):
    path = os.path.join(OUT_DIR, fp)
    if not os.path.exists(path): return [], ""
    with open(path,"r",encoding="utf-8") as f: c = f.read()
    pages = re.split(r'=====\s*第\s*(\d+)\s*页\s*=====', c)
    result = []
    for i in range(1, len(pages), 2):
        n,p = pages[i].strip(), pages[i+1].strip() if i+1<len(pages) else ""
        lines = [l for l in p.split("\n") if l.strip()]
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
    ov = [f'<div class="ob"><h2>{cfg["name"]} 考试概览</h2><div class="date">{cfg["examDateLabel"]}</div><div class="og">']
    m = {"填空题":"16分,8题×2分","选择题":"14分,7题含多选","名词解释":"16分,4个×4分","问答题":"24分,4个×6分","计算题":"30分,3题×10分"}
    for line in exam_lines:
        for nm,det in m.items():
            if nm in line and "分" in line:
                sc,dt = det.split(",",1)
                ov.append(f'<div class="oi"><div class="nm">{nm}</div><div class="sc">{sc}</div><div class="dt">{dt}</div></div>')
                break
    ov.append('</div></div>')
    ov.append('<div class="tc"><h3>重点知识</h3><ul>')
    ink=False
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

    # ── 考点内容（带上下标格式）──
    cfg["tpH"] = {}
    for et in cfg["examTopics"]:
        pages = ch_pages.get(et["ch"], [])
        matched = ext_topic(et, pages)
        ch_t = next((c["title"] for c in cfg["chapters"] if c["id"]==et["ch"]), "")
        ttype = TOPIC_TYPES.get(et["topic"],"")
        tcolor = TYPE_COLORS.get(ttype,"#666")
        tag_html = f'<span class="tt" style="background:{tcolor}">{ttype}</span>' if ttype else ""
        parts = [f'<div class="th"><div class="th-top"><h2>{et["topic"]}</h2>{tag_html}</div><div class="src">来源：{ch_t}</div></div>']
        if matched:
            for s in matched:
                parts.append(f'<div class="ts"><div class="sn">第 {s["num"]} 页</div>')
                for line in s["lines"]: parts.append(f'<p>{fmt_sub_super(line)}</p>')
                parts.append('</div>')
        else:
            parts.append(f'<div class="te">参考 {ch_t} 相关内容</div>')
        cfg["tpH"][et["topic"]] = "\n".join(parts)

    # ── 公式（分组）──
    fh = ['<div class="ss"><h3>必背公式</h3>']
    for gname, formulas in FORMULA_GROUPS:
        fh.append(f'<div class="fg"><div class="fg-title">{gname}</div>')
        for nm,tex in formulas: fh.append(f'<div class="fi"><div class="fn">{nm}</div><div class="math">`{tex}`</div></div>')
        fh.append('</div>')
    fh.append('</div>')
    cfg["fH"] = "\n".join(fh)

    # ── 名词解释（完整定义，多行提取，按考点分组）──
    def extract_definitions(pages):
        """从页面中提取完整定义"""
        def_pats = [
            (r'^(.{1,30})(是指|指的是)(.{5,})',    1),  # term before
            (r'^(.{1,25})(称为|称之为|叫做)(.{5,})', 2),  # term after ("X称为Y" => term=Y)
            (r'^(.{2,12})是(.{35,})',              1),  # term before
        ]
        # 行首词（这些不会是定义的开头）
        bad_starts = ["由于","比如","其中","因此","例如","因为","所以","但是","而且",
            "然而","同时","另外","此外","首先","其次","然后","最后","对于","关于",
            "通过","经过","利用","采用","根据","按照","从","在","将","把","被","为",
            "主要","特别","通常","一般","基本","这里","这个","这些","这种",
            "室温","金属","溶液","一个","一些","它们","两种","三类","能量",
            "这里","现在","目前","那时","以后","以后","之前","之后","注意：","当"]
        # 术语末尾词（这些词后面接"是"不构成定义）
        bad_term_end = ["主要","特别","特别","通常","一般","总","就","都",
            "可能","一定","已经","可以","会","要","已","还","也","又","更",
            "很","最","极","较","相当","比较","尤其","甚至","至少","最多"]
        # 术语本身不能是这些词
        bad_terms = ["一类","另一类","一种","另一种","此外","因此","所谓",
            "用于","就是","可以说","同时","这里"]
        results = []
        for p in pages:
            ls = p["lines"]
            for i, line in enumerate(ls):
                s = line.strip()
                if len(s) < 15: continue
                if re.match(r'^[\d\s\.,;:\-+*/%°()\[\]{}]+$', s): continue
                # 跳过非定义行首
                if any(s.startswith(b) for b in bad_starts): continue
                # 跳过编号开头
                if re.match(r'^[\d①⑴①②③④⑤⑥]', s): continue
                # 跳过可能包含"第"的行（章节标题）
                if re.match(r'^第[一二三四五六七八九十\d]', s): continue
                # 匹配定义模式
                term_name = None
                matched = None
                for pat, grp in def_pats:
                    m = re.search(pat, s)
                    if m:
                        matched = pat
                        if grp == 1:
                            term_name = m.group(1).strip()
                        elif grp == 2:
                            # "称为/叫做"：术语在关键词后面
                            after = m.group(3).strip()
                            term_name = re.split(r'[，。；,.;]', after)[0].strip()
                            if len(term_name) > 20:
                                term_name = after[:20]
                        break
                if not matched or not term_name: continue
                # 清洗术语名
                term_name = term_name.strip().lstrip("：:、；，。；,.;-—")
                # 过滤
                if len(term_name) < 2: continue
                if term_name in bad_terms: continue
                if any(term_name.endswith(b) for b in bad_term_end): continue
                if re.match(r'^[\d]+', term_name): continue
                if re.match(r'^[A-Za-z]{1,2}$', term_name): continue  # 纯字母缩写
                # 收集多行定义
                def_lines = [s]
                for j in range(1, min(3, len(ls)-i)):
                    nl = ls[i+j].strip()
                    if not nl or len(nl) < 3: break
                    if re.match(r'^.{1,20}(是指|称为|叫做|是.{15})', nl): break
                    if re.match(r'^第[一二三四五六七八九十]|^\d+\.|^===|^http', nl): break
                    def_lines.append(nl)
                full_def = "".join(def_lines)
                if len(full_def) < 20: continue
                results.append((term_name, full_def, p["num"]))
        return results

    seen_terms = set()
    topic_terms = {et["topic"]: [] for et in cfg["examTopics"]}
    for et in cfg["examTopics"]:
        pages = ch_pages.get(et["ch"], [])
        defs = extract_definitions(pages)
        for tn, fd, pn in defs:
            key = tn[:8]  # 用术语前8字去重
            if key not in seen_terms:
                seen_terms.add(key)
                topic_terms[et["topic"]].append((tn, fd, pn))

    th = ['<div class="ss"><h3>名词解释（按考点分类）</h3>']
    term_count = 0
    for et in cfg["examTopics"]:
        terms = topic_terms.get(et["topic"], [])
        if not terms: continue
        term_count += len(terms)
        ttype = TOPIC_TYPES.get(et["topic"],"")
        tcol = {"填空":"#4361ee","选择":"#06d6a0","计算":"#e63946","问答":"#f77f00"}.get(ttype.split("/")[0],"#888")
        th.append(f'<div class="tg"><div class="tg-h"><span class="tg-title">{et["topic"]}</span><span class="tg-badge" style="background:{tcol}">{ttype}</span></div>')
        for tn, fd, pn in terms:
            th.append(f'<div class="ti"><span class="ti-term">{fmt_sub_super(tn)}</span><span class="ti-ref">第{pn}页</span><span class="ti-def">{fmt_sub_super(fd)}</span></div>')
        th.append('</div>')
    th.append('</div>')
    cfg["tH"] = "\n".join(th)
    print(f"  考点 {len(cfg['examTopics'])} 个, 名词 {term_count} 个")


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
.sb{width:220px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);position:sticky;top:48px;height:calc(100vh - 48px);overflow-y:auto;padding:4px 0}
.sb::-webkit-scrollbar{width:4px}
.sb::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
.sb .st{padding:4px 12px 2px;font-size:.65em;color:var(--text2);font-weight:600}
.sb .it{display:block;padding:4px 12px 4px 16px;color:var(--text);text-decoration:none;font-size:.8em;border-left:3px solid transparent;cursor:pointer;transition:all .1s}
.sb .it:hover{background:var(--plight);color:var(--primary)}
.sb .it.act{background:var(--plight);color:var(--primary);border-left-color:var(--primary);font-weight:600}
.sb .tp{padding-left:18px;font-size:.78em}
.sb .tag{display:inline-block;font-size:.6em;padding:0 5px;border-radius:8px;color:#fff;margin-left:4px;font-weight:500;vertical-align:middle;line-height:1.5}
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
.th{margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--primary)}
.th-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.th h2{font-size:1.15em;color:var(--primary)}
.tt{display:inline-block;font-size:.65em;color:#fff;padding:1px 10px;border-radius:10px;font-weight:600;letter-spacing:.03em}
.th .src{font-size:.78em;color:var(--text2);margin-top:3px}
.ts{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px 14px;margin-bottom:7px}
.ts .sn{font-size:.7em;color:var(--text2);margin-bottom:3px;font-weight:600}
.ts p{margin-bottom:2px;font-size:.88em}
.ts p sub{font-size:.8em;color:var(--text)}
.ts p sup{font-size:.8em;color:var(--text)}
.ss{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;margin-bottom:14px}
.ss h3{font-size:.9em;color:var(--primary);margin-bottom:10px;padding-bottom:4px;border-bottom:1px solid var(--border)}
.fg{margin-bottom:12px}
.fg-title{font-size:.82em;font-weight:600;color:var(--text2);margin-bottom:6px;padding-left:2px}
.fi{background:var(--plight);border-left:3px solid var(--primary);padding:8px 12px;border-radius:6px;margin-bottom:6px}
.fi .fn{font-size:.75em;color:var(--text2);margin-bottom:2px}
.fi .math{font-size:1.05em;padding:2px 0}
/* 名词分组 */
.tg{margin-bottom:14px;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
.tg-h{display:flex;align-items:center;gap:8px;padding:8px 14px;background:var(--bg);border-bottom:1px solid var(--border)}
.tg-title{font-size:.82em;font-weight:600;color:var(--primary)}
.tg-badge{font-size:.65em;color:#fff;padding:0 8px;border-radius:8px;font-weight:500}
.ti{padding:7px 14px;border-bottom:1px solid #f0f0f0;background:var(--surface)}
.ti:last-child{border-bottom:none}
.ti-term{font-weight:600;color:var(--accent);font-size:.82em;display:block;margin-bottom:1px}
.ti-ref{font-size:.65em;color:var(--text2);float:right;margin-top:-1.2em}
.ti-def{display:block;font-size:.8em;color:var(--text);line-height:1.5}
.ti-def sub,.ti-def sup{font-size:.75em}
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
const TC = %TYPES%;
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
  setTimeout(function(){document.querySelectorAll('.math').forEach(function(el){try{katex.render(el.textContent.slice(1,-1),el,{displayMode:false})}catch(e){}})},100);
  nav('overview');
}

function rs(){
  var s=document.getElementById('sidebar');
  var h='<div class="st">概览</div><a class="it act" data-t="overview" onclick="nav(\'overview\')">考试概览</a>';
  h+='<div class="st">考点复习</div>';
  C.examTopics.forEach(function(t,i){
    var tp=TC[t.topic]||'';
    var col={'填空':'#4361ee','选择':'#06d6a0','计算':'#e63946','问答':'#f77f00','填空/选择':'#4361ee','选择/填空':'#06d6a0','填空/计算':'#4361ee','计算/选择':'#e63946','问答/填空':'#f77f00','问答/计算':'#f77f00','填空/问答':'#4361ee'}[tp]||'#888';
    h+='<a class="it tp" data-t="topic-'+i+'" onclick="nav(\'topic-'+i+'\')">'+t.topic+(tp?'<span class="tag" style="background:'+col+'">'+tp+'</span>':'')+'</a>';
  });
  h+='<div class="st">专题</div><a class="it" data-t="formulas" onclick="nav(\'formulas\')">公式</a><a class="it" data-t="terms" onclick="nav(\'terms\')">名词解释</a>';
  s.innerHTML=h;
}

function rm(){
  var m=document.getElementById('main');
  var h='<div id="s-overview" class="bl act">'+C.ovHTML+'</div>';
  C.examTopics.forEach(function(t,i){h+='<div id="s-topic-'+i+'" class="bl">'+(C.tpH[t.topic]||'')+'</div>';});
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

function td(){document.body.classList.toggle('dark-mode');var b=document.getElementById('dtBtn');b.textContent=document.body.classList.contains('dark-mode')?'☀️':'🌙';localStorage.setItem('rd',document.body.classList.contains('dark-mode')?'1':'0');}
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
    print("复习网页生成器 v5")
    print("="*40)
    for sid, cfg in SUBJECTS.items(): build(sid, cfg)
    # Inject type data alongside subject data
    h = HTML.replace("%DATA%", json.dumps(SUBJECTS, ensure_ascii=False))
    h = h.replace("%TYPES%", json.dumps(TOPIC_TYPES, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8") as f: f.write(h)
    print(f"\n生成: {HTML_OUT} ({os.path.getsize(HTML_OUT)/1024:.0f} KB)")

if __name__ == "__main__":
    main()
