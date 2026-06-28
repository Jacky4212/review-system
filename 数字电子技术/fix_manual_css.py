#!/usr/bin/env python3
"""Add missing side-nav CSS to manually written pages."""
import os

base = "D:/code/cherry studio/复习/数字电子技术"
files = ['ch03.html', 'ch07.html', 'ch10.html', 'chips.html']

# The CSS block to add (before </style>)
nav_css = '''
  /* Right-side chapter nav panel */
  .chapter-nav-toggle {
    position: fixed; right: 0; top: 50%; transform: translateY(-50%);
    width: 36px; height: 36px; border-radius: 8px 0 0 8px;
    background: var(--primary); color: #fff; border: none;
    font-size: 1.2em; cursor: pointer; z-index: 98;
    opacity: 0.8; box-shadow: -2px 0 8px rgba(0,0,0,0.15);
    display: flex; align-items: center; justify-content: center;
  }
  .chapter-nav-toggle:hover { opacity: 1; }
  .chapter-nav-panel {
    position: fixed; right: -200px; top: 50%; transform: translateY(-50%);
    width: 180px; background: var(--card-bg); border-radius: 8px 0 0 8px;
    box-shadow: -4px 0 16px rgba(0,0,0,0.12); z-index: 97;
    transition: right 0.3s ease; padding: 12px 0; max-height: 80vh; overflow-y: auto;
  }
  .chapter-nav-panel.open { right: 0; }
  .chapter-nav-panel .nav-title {
    font-size: 0.8em; color: var(--text-light); padding: 4px 16px 8px;
    border-bottom: 1px solid var(--border); margin-bottom: 6px; font-weight: 600;
  }
  .chapter-nav-panel a {
    display: block; padding: 6px 16px; font-size: 0.85em;
    color: var(--text); text-decoration: none;
    border-left: 3px solid transparent;
  }
  .chapter-nav-panel a:hover { background: var(--code-bg); border-left-color: var(--accent); }
  .chapter-nav-panel a.current { border-left-color: var(--accent); font-weight: 600; }
  .back2top { right: 50px; }
'''

for fname in files:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has the nav CSS
    if 'chapter-nav-toggle' in content and 'right: 50px' not in content:
        # Add the back2top position fix
        content = content.replace('.back2top { right: 30px;', '.back2top { right: 50px;')
        content = content.replace('.back2top:hover { opacity: 1; }', '.back2top:hover { opacity: 1; }\n' + nav_css)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{fname}: updated")
    elif 'chapter-nav-toggle' in content and 'right: 50px' in content:
        print(f"{fname}: already has everything")
    else:
        print(f"{fname}: needs manual check - no toggle button")
