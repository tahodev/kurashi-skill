#!/usr/bin/env python3
from pathlib import Path
import ast, re, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
files=[root/'README.md',*root.glob('*/SKILL.md'),*root.glob('docs/**/*.md')]
failed=False; checked=0; executed=0
# Syntax-check every supported fence. Execute only self-contained, offline snippets;
# network examples are exercised by check-urls.py instead.
unsafe=re.compile(r'\b(curl|wget|npx|npm|gh|git|rm|mv|cp|jq|grep|sed|awk|cat|ls|find|unzip)\b|https?://|/tmp/|\{[A-Z][A-Z0-9_]*\}|\$\{?[A-Z_][A-Z0-9_]*\}?|\b(open|read_text|read_bytes|Image\.open)\s*\(')
for path in files:
    text=path.read_text(encoding='utf-8')
    for i,m in enumerate(re.finditer(r'^```(bash|sh|python|py)\s*\n(.*?)^```\s*$',text,re.M|re.S),1):
        lang,src=m.group(1),m.group(2); checked+=1
        try:
            if lang in ('python','py'): ast.parse(src)
            else:
                p=subprocess.run(['bash','-n'],input=src,text=True,capture_output=True)
                if p.returncode: raise SyntaxError(p.stderr.strip())
        except Exception as e:
            print(f'FAIL  {path.relative_to(root)} code block {i}: {e}'); failed=True; continue
        if not unsafe.search(src) and len(src)<8000:
            cmd=['python3','-I'] if lang in ('python','py') else ['bash','--noprofile','--norc']
            try:
                p=subprocess.run(cmd,input=src,text=True,capture_output=True,timeout=10,cwd=tempfile.gettempdir(),env={'PATH':'/usr/bin:/bin','HOME':tempfile.gettempdir()})
                if p.returncode:
                    print(f'FAIL  {path.relative_to(root)} code block {i} execution: {(p.stderr or p.stdout).strip()[:400]}'); failed=True
                else: executed+=1
            except subprocess.TimeoutExpired:
                print(f'FAIL  {path.relative_to(root)} code block {i}: execution timed out'); failed=True
print(f'OK    syntax-checked {checked} code blocks; executed {executed} self-contained offline blocks')
sys.exit(1 if failed else 0)
