#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import re, subprocess, sys
root=Path(__file__).resolve().parents[1]
MAX_WORKERS=8; TIMEOUT=20
WARN_HOSTS={
    'www.jma.go.jp','www8.cao.go.jp','www.soumu.go.jp','www.nta.go.jp',
    'www.bunka.go.jp','hinanmap.gsi.go.jp','www.kyoshin.bosai.go.jp',
    'eco.mtk.nao.ac.jp','www.post.japanpost.jp','www.e-stat.go.jp','api.e-stat.go.jp',
}
OPENAPI_HOSTS={'api.e-stat.go.jp','api.calil.jp'}
EXCLUDE_URLS={
    'https://www.jma.go.jp/bosai/quake/data/20260908234330_20260908234052_VXSE5k_1.json',
    'https://www.jma.go.jp/bosai/typhoon/data/list.json',
}
url_re=re.compile(r'https?://[^\s)"`\'。，、；：（）<>]+')
placeholders={
    'ESTAT_APP_ID':'INVALID_CI_KEY','CALIL_APPKEY':'INVALID_CI_KEY',
    'SESSION_ID':'INVALID_CI_SESSION','href':'utf/zip/utf_ken_all.zip','BASE_DATE':'20260919',
    'basetime':'20260919000000','validtime':'20260919000000',
    'z':'5','x':'28','y':'12',
}
items={}
for path in root.glob('*/SKILL.md'):
    for raw in url_re.findall(path.read_text(encoding='utf-8')):
        url=raw.rstrip('.,;。,)')
        items.setdefault(url,set()).add(str(path.relative_to(root)))

def materialize(url):
    unresolved=False
    def sub_braced(m):
        nonlocal unresolved
        key=m.group(1)
        if key not in placeholders: unresolved=True; return m.group(0)
        return placeholders[key]
    url=re.sub(r'\$?\{([A-Za-z_][A-Za-z0-9_]*)\}',sub_braced,url)
    url=url.replace('SESSION_ID', placeholders['SESSION_ID'])
    return None if unresolved else url

def host(url): return re.match(r'https?://([^/:]+)',url).group(1).lower()
def in_hosts(h, hosts): return any(h==x or h.endswith('.'+x) for x in hosts)
def api_error(body):
    pats=[r'ERROR-[0-9]+',r'"(?:resultCode|returnCode)"\s*:\s*"?(?!00\b|INFO-000\b|0\b)([A-Z0-9_-]+)',r'<resultCode>\s*(?!00<)([^<]+)']
    for pat in pats:
        m=re.search(pat,body,re.I)
        if m: return m.group(0)[:120]
    return None

def check(pair):
    original,owners=pair; owner=', '.join(sorted(owners))
    if original in EXCLUDE_URLS: return ('SKIP',f'{owner}: {original} (documented transient example)')
    url=materialize(original)
    if not url: return ('SKIP',f'{owner}: {original} (runtime variable)')
    h=host(url)
    try:
        p=subprocess.run(['curl','-sS','-L','--connect-timeout','8','--max-time',str(TIMEOUT),'-A','kurashi-skill-health-check/1.0','-w','\n%{http_code}',url],capture_output=True,timeout=TIMEOUT+5)
        out=p.stdout.decode('utf-8','replace'); body,_,code=out.rpartition('\n'); code=code.strip() or '000'
    except subprocess.TimeoutExpired: body=''; code='000'
    templated=original!=url
    if in_hosts(h,WARN_HOSTS) and (code=='000' or not code.startswith(('2','3'))):
        return ('WARN',f'{owner}: {code} {original} (known CI geo/network restriction)')
    if code=='000': return ('FAIL',f'{owner}: 000 {original}')
    if code.startswith(('2','3')):
        err=api_error(body[:200000])
        if err:
            if templated and in_hosts(h,OPENAPI_HOSTS): return ('OK',f'{owner}: {code} {original} (template probe returned expected API status: {err})')
            return ('FAIL',f'{owner}: {code} {original} (API-level error: {err})')
        return ('OK',f'{owner}: {code} {original}')
    if code in ('400','401','403','404') and templated and in_hosts(h,OPENAPI_HOSTS):
        return ('OK',f'{owner}: {code} {original} (endpoint exists; auth/parameters required)')
    return ('FAIL',f'{owner}: {code} {original}')

failed=False
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures=[pool.submit(check,x) for x in items.items()]
    for future in as_completed(futures):
        status,msg=future.result(); print(f'{status:5} {msg}'); failed |= status=='FAIL'
print(f'Checked {len(items)} unique URLs with {MAX_WORKERS} workers and {TIMEOUT}s/request cap')
sys.exit(1 if failed else 0)
