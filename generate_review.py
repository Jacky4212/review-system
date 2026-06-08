"""
生成复习网页生成器
功能：读取提取的PPT文本和考试要点，生成多科目可扩展的复习HTML
"""

import os
import json
import re

OUT_DIR = r"D:\code\cherry studio\复习\output"
HTML_OUT = r"D:\code\cherry studio\复习\index.html"
EXAM_FILE = os.path.join(OUT_DIR, "考试要点.txt")
CHAPTER_FILES = {}  # 由扫描自动填充

# ─── 科目配置（未来新增科目只需在这里添加） ───
SUBJECTS = {
    "radiochemistry": {
        "name": "放射化学",
        "nameEn": "Radiochemistry",
        "examDate": "2026年6月18日",
        "chapters": [
            {"id": "ch1",  "file": "1.第一章 绪论 (2026)-1(2).txt",             "title": "第一章 绪论", "exam": ["学科特点"]},
            {"id": "ch2",  "file": "2.第二章 放射性(2026)-1.txt",               "title": "第二章 放射性", "exam": ["衰变公式", "半衰期与衰变常数", "衰变类型", "贝克和居里", "比活度", "平衡公式"]},
            {"id": "ch3",  "file": "3.第三章 放射性核素的物理化学.txt",          "title": "第三章 放射性核素的物理化学", "exam": ["同位素效应", "胶体判定", "吸附"]},
            {"id": "ch4",  "file": "4.第四章 物质的分离.txt",                    "title": "第四章 物质的分离", "exam": ["共沉淀", "同二晶", "电化学", "载体", "萃取", "离子交换"]},
            {"id": "ch5",  "file": "6. 天然核素-1.txt",                          "title": "第六章 天然放射性元素化学", "exam": ["天然放射性系", "天然放射性元素"]},
            {"id": "ch6",  "file": "7. 第七章 锕系理论(2).txt",                  "title": "第七章 锕系理论", "exam": ["核反应式", "镭氡计算", "铀钚转化"]},
            {"id": "ch7",  "file": "8.第八章(2).txt",                            "title": "第八章 裂片元素及活化产物化学", "exam": []},
            {"id": "ch8",  "file": "9.第九章 放射性核素的制备.txt",              "title": "第九章 放射性核素的制备", "exam": ["核素制备", "分析方法"]},
        ]
    }
    # 未来新增科目示例：
    # "organic-chemistry": {
    #     "name": "有机化学",
    #     "nameEn": "Organic Chemistry",
    #     "examDate": "2026年7月",
    #     "chapters": [
    #         {"id": "oc1", "file": "有机化学_第一章.txt", "title": "第一章 ...", "exam": [...]},
    #     ]
    # }
}


def load_text(filepath):
    """读取提取的PPT文本"""
    path = os.path.join(OUT_DIR, filepath)
    if not os.path.exists(path):
        return [], f"文件未找到: {filepath}"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # 按页分割
    pages = re.split(r'=====\s*第\s*(\d+)\s*页\s*=====', content)
    # pages[0] 是来源信息，之后交替出现 页码 和 内容
    result = []
    header = pages[0].strip() if pages else ""
    for i in range(1, len(pages), 2):
        page_num = pages[i].strip() if i < len(pages) else ""
        page_content = pages[i + 1].strip() if i + 1 < len(pages) else ""
        # 过滤掉仅含标题行或过短的内容
        lines = [l for l in page_content.split("\n") if l.strip()]
        if lines:
            result.append({"num": page_num, "lines": lines})
    return result, header


def load_exam_requirements():
    """读取考试要求"""
    if not os.path.exists(EXAM_FILE):
        return []
    with open(EXAM_FILE, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def extract_formulas(pages):
    """从页面内容中提取可能的公式行"""
    formulas = []
    for page in pages:
        for line in page["lines"]:
            # 包含常见公式特征的行
            if any(k in line for k in ["=", "公式", "律", "ln", "lg", "exp", "λ", "×10", "E=", "A=", "N="]):
                if len(line) > 5 and len(line) < 120:
                    formulas.append(line)
    return formulas


def extract_key_terms(pages):
    """提取可能的名词解释（短行，带定义性质）"""
    terms = []
    for page in pages:
        for i, line in enumerate(page["lines"]):
            line = line.strip()
            # 以"是指"、"称为"、"即"结尾或包含这些词的定义句
            if any(k in line for k in ["是指", "称为", "叫做", "指的是", "即"]) and 8 < len(line) < 100:
                terms.append(line)
            # 冒号分隔的名词解释
            elif "：" in line and len(line) < 80 and "。" not in line[:line.index("：")]:
                parts = line.split("：", 1)
                if len(parts) == 2 and len(parts[0]) < 20:
                    terms.append(line)
    return terms


# ─── HTML 模板 ───

HTML_HEADER = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>复习系统 | Review</title>
<style>
  :root {
    --bg: #f8f9fa;
    --surface: #ffffff;
    --text: #1a1a2e;
    --text-secondary: #555;
    --primary: #4361ee;
    --primary-light: #eef0ff;
    --accent: #f72585;
    --border: #dee2e6;
    --success: #06d6a0;
    --warning: #ffd166;
    --sidebar-width: 280px;
    --radius: 12px;
    --shadow: 0 2px 12px rgba(0,0,0,0.08);
    --font: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", system-ui, sans-serif;
    --font-mono: "Cascadia Code", "JetBrains Mono", "Fira Code", Consolas, monospace;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html { scroll-behavior: smooth; scroll-padding-top: 80px; }
  body {
    font-family: var(--font);
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    font-size: 15px;
  }

  /* ─── 科目选择页（首页） ─── */
  .subject-selector {
    display: none;
    max-width: 800px;
    margin: 60px auto;
    padding: 0 24px;
  }
  .subject-selector.active { display: block; }
  .subject-selector h1 {
    font-size: 2.2em;
    text-align: center;
    margin-bottom: 8px;
    color: var(--primary);
  }
  .subject-selector .subtitle {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: 40px;
    font-size: 1em;
  }
  .subject-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 20px;
  }
  .subject-card {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 24px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: var(--shadow);
  }
  .subject-card:hover {
    border-color: var(--primary);
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(67, 97, 238, 0.15);
  }
  .subject-card h3 { font-size: 1.2em; margin-bottom: 4px; }
  .subject-card .en { font-size: 0.85em; color: var(--text-secondary); }
  .subject-card .meta { margin-top: 12px; font-size: 0.85em; color: var(--text-secondary); }
  .subject-card .badge {
    display: inline-block;
    background: var(--primary-light);
    color: var(--primary);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8em;
    margin-top: 8px;
  }
  .add-subject-card {
    border: 2px dashed var(--border);
    background: transparent;
    box-shadow: none;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    font-size: 1em;
    min-height: 140px;
    cursor: default;
  }
  .add-subject-card:hover { transform: none; border-color: var(--border); }

  /* ─── 复习页面 ─── */
  .review-page { display: none; }
  .review-page.active { display: block; }

  /* 顶部导航 */
  .top-bar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 20px;
    height: 56px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .top-bar .back-btn {
    background: none;
    border: none;
    font-size: 1.3em;
    cursor: pointer;
    color: var(--primary);
    padding: 4px 8px;
    border-radius: 6px;
    transition: background 0.2s;
  }
  .top-bar .back-btn:hover { background: var(--primary-light); }
  .top-bar .title-area { font-size: 1em; font-weight: 600; }
  .top-bar .title-area .en { font-weight: 400; color: var(--text-secondary); font-size: 0.85em; }
  .top-bar .exam-badge {
    margin-left: auto;
    background: var(--accent);
    color: #fff;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8em;
    font-weight: 500;
  }

  /* 主体布局 */
  .layout {
    display: flex;
    max-width: 1400px;
    margin: 0 auto;
    min-height: calc(100vh - 56px);
  }

  /* 侧边栏 */
  .sidebar {
    width: var(--sidebar-width);
    flex-shrink: 0;
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 16px 0;
    position: sticky;
    top: 56px;
    height: calc(100vh - 56px);
    overflow-y: auto;
  }
  .sidebar::-webkit-scrollbar { width: 4px; }
  .sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

  .sidebar-section { margin-bottom: 8px; }
  .sidebar-section-title {
    padding: 8px 20px 4px;
    font-size: 0.75em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    font-weight: 600;
  }
  .sidebar-item {
    display: block;
    padding: 7px 20px 7px 24px;
    color: var(--text);
    text-decoration: none;
    font-size: 0.92em;
    border-left: 3px solid transparent;
    transition: all 0.15s;
    cursor: pointer;
    position: relative;
  }
  .sidebar-item:hover { background: var(--primary-light); color: var(--primary); }
  .sidebar-item.active {
    background: var(--primary-light);
    color: var(--primary);
    border-left-color: var(--primary);
    font-weight: 600;
  }
  .sidebar-item .exam-tag {
    display: inline-block;
    font-size: 0.65em;
    background: var(--accent);
    color: #fff;
    padding: 0 6px;
    border-radius: 8px;
    margin-left: 4px;
    vertical-align: middle;
  }
  .sidebar-item .ch-num {
    display: inline-block;
    width: 22px;
    height: 22px;
    line-height: 22px;
    text-align: center;
    border-radius: 50%;
    background: var(--bg);
    font-size: 0.75em;
    font-weight: 600;
    margin-right: 6px;
    color: var(--text-secondary);
  }
  .sidebar-item.active .ch-num { background: var(--primary); color: #fff; }

  /* 主内容区 */
  .main-content {
    flex: 1;
    padding: 32px 40px 60px;
    min-width: 0;
  }

  /* 考试概览 */
  .exam-overview {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    border-radius: var(--radius);
    padding: 32px 36px;
    margin-bottom: 32px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  }
  .exam-overview h2 { font-size: 1.5em; margin-bottom: 6px; }
  .exam-overview .exam-date { opacity: 0.85; font-size: 0.9em; margin-bottom: 20px; }
  .exam-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
  }
  .exam-type {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(4px);
    border-radius: 8px;
    padding: 12px 16px;
  }
  .exam-type .name { font-size: 0.85em; opacity: 0.9; }
  .exam-type .score { font-size: 1.6em; font-weight: 700; }
  .exam-type .detail { font-size: 0.75em; opacity: 0.75; }

  .exam-tips {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin-bottom: 32px;
    box-shadow: var(--shadow);
  }
  .exam-tips h3 { color: var(--primary); margin-bottom: 8px; font-size: 1em; }
  .exam-tips ul { padding-left: 20px; }
  .exam-tips li { margin-bottom: 4px; color: var(--text-secondary); font-size: 0.92em; }

  /* 章节内容块 */
  .chapter-block {
    display: none;
    animation: fadeIn 0.3s ease;
  }
  .chapter-block.active { display: block; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

  .chapter-header {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--primary);
  }
  .chapter-header h2 { font-size: 1.5em; color: var(--primary); }
  .chapter-header .exam-topics {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
  }
  .chapter-header .exam-topic-tag {
    background: var(--accent);
    color: #fff;
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 0.78em;
  }
  .chapter-header .no-exam {
    font-size: 0.85em;
    color: var(--text-secondary);
  }

  /* 幻灯片内容卡片 */
  .slide-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: box-shadow 0.2s;
  }
  .slide-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }

  .slide-header {
    padding: 10px 18px;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    font-size: 0.82em;
    font-weight: 600;
    color: var(--text-secondary);
    cursor: pointer;
    user-select: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .slide-header:hover { background: var(--primary-light); }
  .slide-header .toggle-icon { transition: transform 0.2s; font-size: 0.8em; }
  .slide-header.collapsed .toggle-icon { transform: rotate(-90deg); }

  .slide-body {
    padding: 14px 18px;
    line-height: 1.9;
    font-size: 0.95em;
  }
  .slide-body.collapsed { display: none; }

  .slide-body p { margin-bottom: 6px; }
  .slide-body .formula-line {
    font-family: var(--font-mono);
    background: var(--primary-light);
    padding: 6px 12px;
    border-radius: 6px;
    margin: 6px 0;
    font-size: 0.95em;
    border-left: 3px solid var(--primary);
  }
  .slide-body .highlight {
    background: #fff3cd;
    padding: 0 3px;
    border-radius: 3px;
  }
  .slide-body .key-term {
    color: var(--accent);
    font-weight: 600;
  }

  .slide-body .img-placeholder {
    display: inline-block;
    background: var(--bg);
    border: 1px dashed var(--border);
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 0.82em;
    color: var(--text-secondary);
    margin: 4px 0;
  }

  /* 专题区块（公式、名词） */
  .special-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
  }
  .special-section h3 {
    font-size: 1.15em;
    color: var(--primary);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }
  .special-section .item {
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
  }
  .special-section .item:last-child { border-bottom: none; }

  /* 无内容提示 */
  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
  }
  .empty-state .icon { font-size: 3em; margin-bottom: 12px; }
  .empty-state p { font-size: 1em; }

  /* 公式专题 */
  .formula-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
  }
  .formula-item {
    background: var(--primary-light);
    border-left: 3px solid var(--primary);
    padding: 10px 14px;
    border-radius: 6px;
    font-family: var(--font-mono);
    font-size: 0.9em;
    line-height: 1.6;
  }

  /* 名词专题 */
  .term-item {
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
  }
  .term-item:last-child { border-bottom: none; }
  .term-item .term-name {
    font-weight: 600;
    color: var(--accent);
  }

  /* 响应式 */
  @media (max-width: 900px) {
    .sidebar { display: none; }
    .main-content { padding: 20px; }
    .exam-grid { grid-template-columns: repeat(2, 1fr); }
    .formula-grid { grid-template-columns: 1fr; }
  }
  @media (max-width: 500px) {
    .exam-grid { grid-template-columns: 1fr; }
    .exam-overview { padding: 20px; }
  }

  /* 移动端侧栏切换 */
  .mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    font-size: 1.2em;
    cursor: pointer;
    color: var(--primary);
    padding: 4px 8px;
  }
  @media (max-width: 900px) {
    .mobile-menu-btn { display: block; }
  }
  .sidebar-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: 200;
  }
  .sidebar-overlay.show { display: block; }
  .sidebar.mobile-show {
    display: block;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 300;
    height: 100vh;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
  }
</style>
</head>
<body>

<!-- ═══ 科目选择页 ═══ -->
<div id="subjectSelector" class="subject-selector active">
  <h1>📚 复习系统</h1>
  <p class="subtitle">选择科目开始复习</p>
  <div class="subject-cards">
    <!-- 由 JS 动态生成 -->
  </div>
</div>

<!-- ═══ 复习页面 ═══ -->
<div id="reviewPage" class="review-page">

  <!-- 顶栏 -->
  <div class="top-bar">
    <button class="back-btn" onclick="showSubjectSelector()" title="返回科目选择">←</button>
    <button class="mobile-menu-btn" onclick="toggleMobileSidebar()">☰</button>
    <div class="title-area">
      <span id="subjectTitle">放射化学</span>
      <span class="en" id="subjectTitleEn">Radiochemistry</span>
    </div>
    <span class="exam-badge" id="examBadge">📅 6月18日考试</span>
  </div>

  <!-- 遮罩 -->
  <div id="sidebarOverlay" class="sidebar-overlay" onclick="toggleMobileSidebar()"></div>

  <div class="layout">
    <!-- 侧边栏 -->
    <nav class="sidebar" id="sidebar">
      <div class="sidebar-section">
        <div class="sidebar-section-title">概览</div>
        <a class="sidebar-item active" data-target="overview" onclick="navigateTo('overview')">
          📋 考试概览
        </a>
      </div>
      <div class="sidebar-section" id="chapterNav">
        <div class="sidebar-section-title">章节复习</div>
        <!-- 由 JS 动态生成 -->
      </div>
      <div class="sidebar-section" id="specialNav">
        <div class="sidebar-section-title">重点专题</div>
        <a class="sidebar-item" data-target="formulas" onclick="navigateTo('formulas')">📐 必背公式</a>
        <a class="sidebar-item" data-target="terms" onclick="navigateTo('terms')">📖 名词解释</a>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="main-content" id="mainContent">
      <!-- 由 JS 动态渲染 -->
    </main>
  </div>
</div>

<script>
// ═══════════════════════════════════════════════════════
//  科目数据（由 Python 生成）
// ═══════════════════════════════════════════════════════

const SUBJECTS = %SUBJECTS_JSON%;

let currentSubject = null;

// ═══ 科目选择 ═══
function showSubjectSelector() {
  document.getElementById('subjectSelector').classList.add('active');
  document.getElementById('reviewPage').classList.remove('active');
  document.title = '复习系统 | Review';
  window.scrollTo(0, 0);
}

function enterSubject(subjectId) {
  currentSubject = SUBJECTS[subjectId];
  document.getElementById('subjectSelector').classList.remove('active');
  document.getElementById('reviewPage').classList.add('active');
  document.title = currentSubject.name + ' | 复习系统';

  // 填充顶栏
  document.getElementById('subjectTitle').textContent = currentSubject.name;
  document.getElementById('subjectTitleEn').textContent = currentSubject.nameEn;
  document.getElementById('examBadge').textContent = '📅 ' + currentSubject.examDate;

  // 渲染侧边栏章节导航
  renderSidebarChapters(currentSubject.chapters);
  // 渲染主内容
  renderMainContent(currentSubject);
  // 默认定位到概览
  navigateTo('overview');
}

function renderSidebarChapters(chapters) {
  const nav = document.getElementById('chapterNav');
  let html = '<div class="sidebar-section-title">章节复习</div>';
  chapters.forEach((ch, i) => {
    const hasExam = ch.exam && ch.exam.length > 0;
    html += '<a class="sidebar-item" data-target="ch-' + ch.id + '" onclick="navigateTo(\'ch-' + ch.id + '\')">'
         + '<span class="ch-num">' + (i+1) + '</span>'
         + ch.title
         + (hasExam ? ' <span class="exam-tag">考</span>' : '')
         + '</a>';
  });
  nav.innerHTML = html;
}

// ═══ 渲染主内容 ═══
function renderMainContent(subject) {
  const container = document.getElementById('mainContent');
  let html = '';

  // --- 考试概览 ---
  html += '<div id="section-overview" class="chapter-block active">';
  html += subject.examOverviewHTML;
  html += '</div>';

  // --- 各章节 ---
  subject.chapters.forEach(ch => {
    html += '<div id="section-ch-' + ch.id + '" class="chapter-block">';
    html += ch.html || '<div class="empty-state"><div class="icon">📄</div><p>内容加载中...</p></div>';
    html += '</div>';
  });

  // --- 重点专题 ---
  html += '<div id="section-formulas" class="chapter-block">';
  html += subject.formulasHTML || '<div class="empty-state"><div class="icon">📐</div><p>暂无公式数据</p></div>';
  html += '</div>';

  html += '<div id="section-terms" class="chapter-block">';
  html += subject.termsHTML || '<div class="empty-state"><div class="icon">📖</div><p>暂无名词数据</p></div>';
  html += '</div>';

  container.innerHTML = html;
}

// ═══ 导航 ═══
function navigateTo(target) {
  // 更新侧边栏状态
  document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
  const sidebarItem = document.querySelector('.sidebar-item[data-target="' + target + '"]');
  if (sidebarItem) sidebarItem.classList.add('active');

  // 显示对应内容
  document.querySelectorAll('.chapter-block').forEach(el => el.classList.remove('active'));
  const section = document.getElementById('section-' + target);
  if (section) {
    section.classList.add('active');
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // 关闭移动端侧边栏
  if (window.innerWidth <= 900) {
    document.getElementById('sidebar').classList.remove('mobile-show');
    document.getElementById('sidebarOverlay').classList.remove('show');
  }
}

function toggleMobileSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  sidebar.classList.toggle('mobile-show');
  overlay.classList.toggle('show');
}

// ═══ 初始化：渲染科目卡片 ═══
function initSubjectCards() {
  const container = document.querySelector('.subject-cards');
  let html = '';
  let first = true;
  for (const [id, sub] of Object.entries(SUBJECTS)) {
    const chCount = sub.chapters.length;
    html += '<div class="subject-card" onclick="enterSubject(\'' + id + '\')">'
         + '<h3>' + sub.name + '</h3>'
         + '<div class="en">' + sub.nameEn + '</div>'
         + '<div class="meta">📚 ' + chCount + ' 章 · 📅 ' + sub.examDate + '</div>'
         + '<div class="badge">点击复习 →</div>'
         + '</div>';
  }
  // 占位卡片
  html += '<div class="subject-card add-subject-card">+ 后续可添加更多科目</div>';
  container.innerHTML = html;
}

initSubjectCards();
</script>
</body>
</html>
"""


def build_subject_data(subject_id, subject_cfg):
    """生成某个科目的完整 HTML 数据"""
    print(f"  正在处理: {subject_cfg['name']}")

    # 加载考试要求
    exam_lines = load_exam_requirements()

    # ---- 构建考试概览 HTML ----
    overview_parts = []
    overview_parts.append('<div class="exam-overview">')
    overview_parts.append(f'<h2>{subject_cfg["name"]} 考试概览</h2>')
    overview_parts.append(f'<div class="exam-date">📅 考试时间：{subject_cfg["examDate"]}</div>')

    # 解析考试题型
    exam_types = []
    current_type = {}
    for line in exam_lines:
        if "填空题" in line and "分" in line:
            exam_types.append({"name": "填空题", "score": "16分", "detail": "8题 × 2分，一空分值不定"})
        elif "选择题" in line and "分" in line:
            exam_types.append({"name": "选择题", "score": "14分", "detail": "7题，含单选和多选，部分答对得分"})
        elif "名词解释" in line and "分" in line:
            exam_types.append({"name": "名词解释", "score": "16分", "detail": "4个 × 4分"})
        elif "问答题" in line and "分" in line:
            exam_types.append({"name": "问答题", "score": "24分", "detail": "4个 × 6分"})
        elif "计算题" in line and "分" in line:
            exam_types.append({"name": "计算题", "score": "30分", "detail": "3题 × 10分，保留两位小数"})

    overview_parts.append('<div class="exam-grid">')
    for et in exam_types:
        overview_parts.append(f'<div class="exam-type"><div class="name">{et["name"]}</div><div class="score">{et["score"]}</div><div class="detail">{et["detail"]}</div></div>')
    overview_parts.append('</div></div>')

    # 注意事项
    tips = [l for l in exam_lines if "注意" in l or "铅笔" in l or "计算器" in l]
    overview_parts.append('<div class="exam-tips"><h3>⚠️ 考试注意事项</h3><ul>')
    for t in tips:
        overview_parts.append(f'<li>{t}</li>')
    overview_parts.append('</ul></div>')

    # 重点知识点列表
    overview_parts.append('<div class="exam-tips"><h3>📌 放射化学重点知识</h3><ul>')
    in_keywords = False
    for line in exam_lines:
        if "重点知识" in line:
            in_keywords = True
            continue
        if in_keywords and ("注意" in line or "铅笔" in line or "计算器" in line or "AI 生成" in line):
            continue
        if in_keywords and line.strip():
            overview_parts.append(f'<li>{line.strip()}</li>')
    overview_parts.append('</ul></div>')

    subject_cfg["examOverviewHTML"] = "\n".join(overview_parts)

    # ---- 处理各章节 ----
    all_formulas = []
    all_terms = []

    for ch in subject_cfg["chapters"]:
        pages, header = load_text(ch["file"])
        if not pages:
            ch["html"] = f'<div class="empty-state"><div class="icon">📄</div><p>{header}</p></div>'
            continue

        # 构建章节 HTML
        parts = []
        parts.append(f'<div class="chapter-header">')
        parts.append(f'<h2>{ch["title"]}</h2>')
        if ch["exam"]:
            topic_tags = "".join(f'<span class="exam-topic-tag">★ {t}</span>' for t in ch["exam"])
            parts.append(f'<div class="exam-topics">{topic_tags}</div>')
        else:
            parts.append(f'<div class="no-exam">📖 了解性内容</div>')
        parts.append('</div>')

        # 幻灯片卡片
        for p in pages:
            parts.append('<div class="slide-card">')
            parts.append(f'<div class="slide-header" onclick="this.classList.toggle(\'collapsed\'); this.nextElementSibling.classList.toggle(\'collapsed\')">')
            parts.append(f'<span>📄 第 {p["num"]} 页</span>')
            parts.append('<span class="toggle-icon">▼</span>')
            parts.append('</div>')
            parts.append('<div class="slide-body">')

            for line in p["lines"]:
                line_escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                # 公式行
                if any(k in line for k in ["=", "ln", "lg", "exp", "λ", "×10", "N=", "A="]) and len(line) < 100 and any(c.isdigit() for c in line):
                    parts.append(f'<div class="formula-line">{line_escaped}</div>')
                else:
                    parts.append(f'<p>{line_escaped}</p>')

            parts.append('</div></div>')

        ch["html"] = "\n".join(parts)

        # 收集公式和名词
        all_formulas.extend(extract_formulas(pages))
        all_terms.extend(extract_key_terms(pages))

    # ---- 重点专题：公式 ----
    formula_html = ['<div class="special-section"><h3>📐 必背公式</h3>']
    formula_html.append('<div class="formula-grid">')
    # 去重并排序
    seen = set()
    for f in all_formulas:
        norm = f.strip()
        if norm and norm not in seen and len(norm) > 3:
            seen.add(norm)
            formula_html.append(f'<div class="formula-item">{norm.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</div>')
    formula_html.append('</div></div>')
    subject_cfg["formulasHTML"] = "\n".join(formula_html)

    # ---- 重点专题：名词解释 ----
    term_html = ['<div class="special-section"><h3>📖 名词解释</h3>']
    seen_terms = set()
    for t in all_terms:
        t = t.strip()
        if t and t not in seen_terms and len(t) > 4:
            seen_terms.add(t)
            # 提取冒号前的名词
            if "：" in t:
                name, desc = t.split("：", 1)
                term_html.append(f'<div class="term-item"><span class="term-name">{name}</span>：{desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</div>')
            else:
                term_html.append(f'<div class="term-item">{t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</div>')
    term_html.append('</div>')
    subject_cfg["termsHTML"] = "\n".join(term_html)

    print(f"   ├─ 章节: {len(subject_cfg['chapters'])} 个")
    print(f"   ├─ 公式: {len(all_formulas)} 条 (去重后 {len(seen)} 条)")
    print(f"   └─ 名词: {len(seen_terms)} 个")


def main():
    print("=" * 50)
    print("复习网页生成器")
    print("=" * 50)

    for sid, scfg in SUBJECTS.items():
        build_subject_data(sid, scfg)

    # 生成最终 HTML
    subjects_json = json.dumps(SUBJECTS, ensure_ascii=False, indent=2)
    html = HTML_HEADER.replace("%SUBJECTS_JSON%", subjects_json)

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)

    file_size = os.path.getsize(HTML_OUT) / 1024
    print(f"\n[OK] 网页已生成: {HTML_OUT}")
    print(f"   文件大小: {file_size:.1f} KB")
    print(f"   科目数: {len(SUBJECTS)}")
    print(f"   总章节: {sum(len(s['chapters']) for s in SUBJECTS.values())}")
    print(f"\n[提示] 直接用浏览器打开 index.html 即可开始复习！")


if __name__ == "__main__":
    main()
