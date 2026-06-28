#!/usr/bin/env python3
"""Restructure page layout with proper flex layout to prevent overlap."""
import os, re

base = "D:/code/cherry studio/复习/数字电子技术"

# New layout CSS
layout_css = '''
  /* ===== Layout ===== */
  body { display: flex; min-height: 100vh; }
  .sidebar {
    position: fixed; top: 0; left: 0; width: 210px; height: 100vh;
    background: #ffffff; border-right: 1px solid #edf2f7;
    z-index: 100; overflow-y: auto;
    display: flex; flex-direction: column; flex-shrink: 0;
  }
  .main-wrap { flex: 1; min-width: 0; margin-left: 210px; display: flex; flex-direction: column; }
  .topbar {
    background: linear-gradient(135deg, var(--primary), var(--accent)); color: #fff; padding: 20px;
    position: sticky; top: 0; z-index: 99;
  }
  .topbar-inner { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; flex: 1; }
  .footer { text-align: center; padding: 20px; color: #94a3b8; font-size: 0.78em; border-top: 1px solid #e8ecf0; }
  @media (max-width: 768px) {
    .sidebar { display: none; }
    .main-wrap { margin-left: 0; }
  }
'''

def wrap_content(html):
    """Wrap page content in main-wrap div."""
    # Find body content between <body> and </body>
    body_start = html.find('<body>')
    body_end = html.find('</body>')
    if body_start < 0 or body_end < 0:
        return html

    inner = html[body_start + 6:body_end]

    # Extract sidebar if it exists
    sidebar_match = re.search(r'<nav class="sidebar">.*?</nav>\n?', inner, re.DOTALL)
    sidebar_html = ''
    if sidebar_match:
        sidebar_html = sidebar_match.group()
        inner = inner.replace(sidebar_match.group(), '')

    # Remove old sidebar CSS and layout rules
    inner = re.sub(r'  \.container \{\n.*?margin-left: 210px;.*?\n  \}\n', '', inner)
    inner = re.sub(r'  \.topbar \{\n.*?left: 210px;.*?\n  \}\n', '', inner)
    inner = re.sub(r'  \.footer \{\n.*?margin-left: 210px;.*?\n  \}\n', '', inner)

    # Remove inline script at end
    script_match = re.search(r'<script>\n\(function\(\)\{.*?\}\);?\(\);\n</script>', inner, re.DOTALL)
    script_html = ''
    if script_match:
        script_html = script_match.group()
        inner = inner.replace(script_match.group(), '')

    # Build new structure
    new_inner = sidebar_html + '\n<div class="main-wrap">\n' + inner.strip() + '\n' + script_html + '\n</div>'

    html = html[:body_start + 6] + '\n' + new_inner + '\n' + html[body_end:]
    return html

# 1. Update generate_chapters.py template
gen_py = os.path.join(base, 'generate_chapters.py')
with open(gen_py, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace old CSS section
sidebar_end = c.find('\n  @media (max-width: 768px)', c.find('/* ===== Left Sidebar'))
if sidebar_end >= 0:
    # Find the end of the sidebar section
    sec_end = c.find('\n\n', sidebar_end)
    if sec_end < 0:
        sec_end = c.find('\n  }', sidebar_end) + 3
    # Also remove subsequent offset rules
    for rule in ['.container { margin-left', '.topbar { left:', '.footer { margin-left:']:
        line_start = c.rfind('\n  ', 0, c.find(rule))
        line_end = c.find('\n', c.find(rule))
        if line_start >= 0 and line_end > line_start:
            pass  # handled by section replacement

    before = c[:c.find('/* ===== Left Sidebar')]
    after_start = c.find('.container { margin-left: 210px;', c.find('/* ===== Left Sidebar'))
    if after_start >= 0:
        after = c[after_start:]
        # Remove the 3 offset rules
        after = re.sub(r'  \.container \{ margin-left: 210px; \}\n', '', after)
        after = re.sub(r'  \.topbar \{ left: 210px; width: calc\(100% - 210px\); \}\n', '', after)
        after = re.sub(r'  \.footer \{ margin-left: 210px; \}\n', '', after)
        c = before + layout_css.strip() + '\n\n' + after

# Replace style in template
c = re.sub(r'  \.topbar \{\n.*?position: sticky;.*?\n.*?\n  \}', '  .topbar {\n    background: linear-gradient(135deg, var(--primary), var(--accent)); color: #fff; padding: 20px;\n    position: sticky; top: 0; z-index: 99;\n  }', c)
c = re.sub(r'  \.topbar-inner \{\n.*?max-width: 1100px;.*?\n.*?\n  \}', '  .topbar-inner { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }', c)
c = re.sub(r'  \.container \{\n.*?max-width: 1100px;.*?\n.*?\n  \}', '  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; flex: 1; }', c)
c = re.sub(r'  \.footer \{\n.*?text-align: center;.*?\n.*?\n  \}', '  .footer { text-align: center; padding: 20px; color: #94a3b8; font-size: 0.78em; border-top: 1px solid #e8ecf0; }', c)

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

    # Replace sidebar CSS section
    c = re.sub(r'\n  /\* ===== Left Sidebar ===== \*/.*?(?=\n  @media|\n\n|\n  \})', '', c, flags=re.DOTALL)
    c = re.sub(r'\n  /\* ===== Layout ===== \*/.*?(?=\n  @media|\n\n|\n  \})', '', c, flags=re.DOTALL)
    c = re.sub(r'\n  \.container \{ margin-left: 210px; \}\n', '', c)
    c = re.sub(r'\n  \.topbar \{ left: 210px; width: calc\(100% - 210px\); \}\n', '', c)
    c = re.sub(r'\n  \.footer \{ margin-left: 210px; \}\n', '', c)

    # Add layout CSS
    if 'Layout' not in c:
        c = c.replace('</style>', layout_css.strip() + '\n</style>')

    # Fix topbar CSS - replace sticky definition
    old_top = '    background: linear-gradient(135deg, var(--primary), var(--accent));\n    color: #fff;\n    padding: 20px;\n    position: sticky;\n    top: 0;\n    z-index: 100;\n    box-shadow: 0 2px 8px rgba(0,0,0,0.15);\n  }'
    new_top = '    background: linear-gradient(135deg, var(--primary), var(--accent)); color: #fff; padding: 20px;\n    position: sticky; top: 0; z-index: 99;\n  }'
    c = c.replace(old_top, new_top)

    # Fix container
    old_con = '  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }'
    new_con = '  .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; flex: 1; }'
    c = c.replace(old_con, new_con)

    # Fix topbar-inner
    old_ti = '  .topbar-inner {\n    max-width: 1100px;\n    margin: 0 auto;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    flex-wrap: wrap;\n    gap: 10px;\n  }'
    c = c.replace(old_ti, '  .topbar-inner { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }')

    # Fix footer
    old_ft = '  .footer {\n    text-align: center;\n    padding: 24px;\n    color: var(--text-light);\n    font-size: 0.85em;\n    border-top: 1px solid var(--border);\n  }'
    new_ft = '  .footer { text-align: center; padding: 20px; color: #94a3b8; font-size: 0.78em; border-top: 1px solid #e8ecf0; }'
    c = c.replace(old_ft, new_ft)

    # Wrap content
    c = wrap_content(c)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"{fname}: updated")

print("All done!")
