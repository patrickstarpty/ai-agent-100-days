"""Check lesson files: headings, required sections, relative links, leftovers.

Usage: python3 scripts/check.py .
"""
import glob
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
REQUIRED = ["**一句话**", "**放在全局看**", "### 学习目标", "### 自检", "### 参考说明"]
# Generic words that should not appear in a public course. Add your own private terms locally; do not commit them.
SUSPECT = re.compile(r"保险|核保|理赔|银行|我们公司|公司内部|本部门")
problems = 0
days = {}
for f in sorted(glob.glob(str(root / "Day*/*.md"))):
    p = pathlib.Path(f)
    text = p.read_text(encoding="utf-8")
    m = re.match(r"(\d+)\.", p.name)
    n = int(m.group(1)) if m else -1
    days[n] = p
    head = re.search(r"^## Day(\d+) - ", text, re.M)
    if not head or int(head.group(1)) != n:
        print(f"HEADING  {f}: expected '## Day{n:02d} - …'"); problems += 1
    retro = "复盘" in p.name
    for key in REQUIRED:
        if key == "### 自检" and retro and "### 阶段验收" in text:
            continue  # wrap-up lessons end with an acceptance checklist instead
        if key not in text:
            print(f"MISSING  {f}: {key}"); problems += 1
    qs = re.search(r"### 自检\n(.*?)(?=\n### |\Z)", text, re.S)
    if qs and len(re.findall(r"^\d+\. ", qs.group(1), re.M)) != 2:
        print(f"SELFTEST {f}: 自检 should have exactly 2 questions"); problems += 1
    if SUSPECT.search(text):
        print(f"SUSPECT  {f}: {sorted(set(SUSPECT.findall(text)))}"); problems += 1
for f in glob.glob(str(root / "**/*.md"), recursive=True):
    p = pathlib.Path(f)
    for m in re.finditer(r"\]\((\.{1,2}/[^)#]+)", p.read_text(encoding="utf-8")):
        if not (p.parent / m.group(1)).resolve().exists():
            print(f"LINK     {f}: {m.group(1)}"); problems += 1
missing = [n for n in range(1, 101) if n not in days]
print(f"written: {len(days)}/100; missing days: {missing}")
print(f"problems: {problems}")
sys.exit(1 if problems else 0)
