#!/usr/bin/env python3
"""Fix: replace ASCII ' that breaks Python strings with proper prime char."""
path = 'D:/code/cherry studio/复习/数字电子技术/试卷/update_answers.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# The issue: combining overline (U+0305) was replaced with ASCII ' (U+0027)
# which terminates Python single-quoted strings

# Replace with Unicode PRIME (U+2032) which won't break strings
PR = '′'  # ′

# Targeted replacements in content strings only
replacements = [
    ("F=AB' (C)", "F=A{B} (C)".format(B=PR)),
    ("K'·Qⁿ", "K{P}·Qⁿ".format(P=PR)),
    ("J·Q'ⁿ", "J·Q{P}ⁿ".format(P=PR)),
    ("B'D'", "B{P}D{P}".format(P=PR)),
    ("C'D'", "C{P}D{P}".format(P=PR)),
    ("A'BC'", "A{P}BC{P}".format(P=PR)),
    ("Q'₁ⁿ", "Q{P}₁ⁿ".format(P=PR)),
    ("Q'₀ⁿ", "Q{P}₀ⁿ".format(P=PR)),
    ("Q'ⁿ", "Q{P}ⁿ".format(P=PR)),
    ("Y'₃", "Y{P}₃".format(P=PR)),
    ("Y'₄", "Y{P}₄".format(P=PR)),
    ("Y'₅", "Y{P}₅".format(P=PR)),
    ("Y'₆", "Y{P}₆".format(P=PR)),
    ("Y'₇", "Y{P}₇".format(P=PR)),
    ("m'i", "m{P}i".format(P=PR)),
    ("J'·Q", "J{P}·Q".format(P=PR)),
    ("K'·Q", "K{P}·Q".format(P=PR)),
    ("(B)F=A", "(B)F=AB{P}".format(P=PR)),
]

for old, new in replacements:
    c = c.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed')
