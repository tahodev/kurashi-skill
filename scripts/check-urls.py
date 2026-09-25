#!/usr/bin/env python3
"""Check every documented URL against explicit response and WARN contracts."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import re, subprocess, sys

root = Path(__file__).resolve().parents[1]
MAX_WORKERS = 8
TIMEOUT = 20
TODAY = date.today()

@dataclass(frozen=True)
class Contract:
    statuses: tuple[int, ...]
    content_types: tuple[str, ...]
    label: str

@dataclass(frozen=True)
class WarnRule:
    reason: str
    expires: date
    budget: int

# Ordered, endpoint-specific contracts. The fallback is for human-facing source/docs pages.
CONTRACTS = [
    (re.compile(r'^https://www\.jma\.go\.jp/bosai/.+\.json(?:\?|$)'), Contract((200,), ('application/json',), 'JMA JSON')),
    (re.compile(r'^https://api\.p2pquake\.net/'), Contract((200,), ('application/json',), 'P2PQuake JSON')),
    (re.compile(r'^https://api\.wolfx\.jp/'), Contract((200,), ('application/json', 'text/plain'), 'Wolfx API')),
    (re.compile(r'^https://api\.calil\.jp/'), Contract((200, 400, 401, 403, 404), ('application/json', 'text/javascript', 'text/plain'), 'Calil API')),
    (re.compile(r'^https://api\.e-stat\.go\.jp/'), Contract((200, 400, 401, 403), ('application/json', 'application/xml', 'text/xml'), 'e-Stat API')),
    (re.compile(r'^https://www8\.cao\.go\.jp/chosei/shukujitsu/.+\.csv'), Contract((200,), ('text/csv', 'application/octet-stream', 'text/plain'), 'Cabinet Office CSV')),
    (re.compile(r'^https://www\.post\.japanpost\.jp/.+\.zip'), Contract((200,), ('application/zip', 'application/octet-stream'), 'Japan Post ZIP')),
    (re.compile(r'^https://raw\.githubusercontent\.com/.+\.csv'), Contract((200,), ('text/plain', 'text/csv'), 'GitHub raw CSV')),
    (re.compile(r'^https://soramame\.env\.go\.jp/data/sokutei/.+\.csv'), Contract((200,), ('text/csv', 'application/octet-stream', 'text/plain'), 'AEROS CSV')),
    (re.compile(r'^https://soramame\.env\.go\.jp/'), Contract((200,), ('application/json', 'text/csv', 'text/plain', 'application/octet-stream'), 'AEROS API')),
    (re.compile(r'^https://www\.wbgt\.env\.go\.jp/api/v1/'), Contract((200,), ('application/json',), 'WBGT API v1')),
    (re.compile(r'^https://www\.wbgt\.env\.go\.jp/man15NH/'), Contract((200,), ('text/csv', 'application/pdf', 'application/octet-stream', 'text/plain'), 'WBGT master/manual')),
    (re.compile(r'^https://dataset\.address-br\.digital\.go\.jp/api/'), Contract((200,), ('application/json',), 'ABR Hub API')),
    (re.compile(r'^https://data\.address-br\.digital\.go\.jp/.+\.zip'), Contract((200,), ('application/zip', 'application/octet-stream'), 'ABR ZIP')),
]
DEFAULT_CONTRACT = Contract(tuple(range(200, 400)), ('text/html', 'text/plain', 'text/csv', 'application/pdf', 'application/json', 'application/octet-stream', 'image/'), 'documentation page')

# A WARN is temporary debt, never an open-ended host allowlist. Budgets are per reason.
WARN_RULES = {
    'ci-geo-network': WarnRule('GitHub-hosted runners may be blocked by Japanese public sites', date(2026, 12, 31), 15),
    'quiet-time-empty-feed': WarnRule('feed legitimately returns 404 when no event is active', date(2026, 10, 31), 1),
}
WARN_HOSTS = {
    'www.jma.go.jp', 'www8.cao.go.jp', 'www.soumu.go.jp', 'www.nta.go.jp',
    'www.bunka.go.jp', 'hinanmap.gsi.go.jp', 'www.kyoshin.bosai.go.jp',
    'eco.mtk.nao.ac.jp', 'www.post.japanpost.jp', 'www.e-stat.go.jp', 'api.e-stat.go.jp',
    'data.address-br.digital.go.jp', 'dataset.address-br.digital.go.jp',
    'soramame.env.go.jp', 'www.wbgt.env.go.jp',
}
QUIET_TIME_URLS = {'https://www.jma.go.jp/bosai/typhoon/data/list.json'}
EXCLUDE_URLS = {'https://www.jma.go.jp/bosai/quake/data/20260908234330_20260908234052_VXSE5k_1.json'}
URL_RE = re.compile(r'https?://[^\s)"`\'。，、；：（）<>]+')
PLACEHOLDERS = {
    'ESTAT_APP_ID': 'INVALID_CI_KEY', 'CALIL_APPKEY': 'INVALID_CI_KEY',
    'SESSION_ID': 'INVALID_CI_SESSION', 'href': 'utf/zip/utf_ken_all.zip',
    'BASE_DATE': '20260919', 'basetime': '20260919000000', 'validtime': '20260919000000',
    'z': '5', 'x': '28', 'y': '12',
}

def source_files():
    return [root / 'README.md', *root.glob('*/SKILL.md'), *root.glob('docs/**/*.md')]

def collect_urls():
    items = {}
    for path in source_files():
        for raw in URL_RE.findall(path.read_text(encoding='utf-8')):
            url = raw.rstrip('.,;。,)')
            items.setdefault(url, set()).add(str(path.relative_to(root)))
    return items

def materialize(url):
    unresolved = False
    def replace(match):
        nonlocal unresolved
        key = match.group(1)
        if key not in PLACEHOLDERS:
            unresolved = True
            return match.group(0)
        return PLACEHOLDERS[key]
    url = re.sub(r'\$?\{([A-Za-z_][A-Za-z0-9_]*)\}', replace, url)
    url = url.replace('SESSION_ID', PLACEHOLDERS['SESSION_ID'])
    return None if unresolved else url

def contract_for(url):
    for pattern, contract in CONTRACTS:
        if pattern.search(url):
            return contract
    return DEFAULT_CONTRACT

def host(url):
    return (urlsplit(url).hostname or '').lower()

def in_hosts(value, hosts):
    return any(value == item or value.endswith('.' + item) for item in hosts)

def api_error(body):
    patterns = [r'ERROR-[0-9]+', r'"(?:resultCode|returnCode)"\s*:\s*"?(?!00\b|INFO-000\b|0\b)([A-Z0-9_-]+)', r'<resultCode>\s*(?!00<)([^<]+)']
    for pattern in patterns:
        match = re.search(pattern, body, re.I)
        if match:
            return match.group(0)[:120]
    return None

def warn(reason, owner, code, original):
    rule = WARN_RULES[reason]
    return 'WARN', f'{owner}: {code} {original} ({reason}: {rule.reason}; expires {rule.expires})', reason

def check(pair):
    original, owners = pair
    owner = ', '.join(sorted(owners))
    if original in EXCLUDE_URLS:
        return 'SKIP', f'{owner}: {original} (documented historical example)', None
    url = materialize(original)
    if not url:
        return 'SKIP', f'{owner}: {original} (unresolved runtime variable)', None
    expected = contract_for(url)
    try:
        proc = subprocess.run([
            'curl', '-sS', '-L', '--connect-timeout', '8', '--max-time', str(TIMEOUT),
            '-A', 'kurashi-skill-health-check/2.0', '-o', '-', '-w', '\n%{http_code}\n%{content_type}', url,
        ], capture_output=True, timeout=TIMEOUT + 5)
        output = proc.stdout.decode('utf-8', 'replace')
        body, _, tail = output.rpartition('\n')
        body, _, code = body.rpartition('\n')
        code, content_type = code.strip() or '000', tail.strip().lower()
    except subprocess.TimeoutExpired:
        body, code, content_type = '', '000', ''
    templated = original != url
    numeric = int(code) if code.isdigit() else 0
    if original in QUIET_TIME_URLS and code == '404':
        return warn('quiet-time-empty-feed', owner, code, original)
    if in_hosts(host(url), WARN_HOSTS) and (code == '000' or numeric not in expected.statuses):
        return warn('ci-geo-network', owner, code, original)
    if numeric not in expected.statuses:
        return 'FAIL', f'{owner}: {code} {original} (expected {expected.label} status {expected.statuses})', None
    # Empty-body 4xx probes can legitimately omit Content-Type; success responses cannot.
    if not content_type and 400 <= numeric < 500 and templated:
        pass
    elif not any(token in content_type for token in expected.content_types):
        return 'FAIL', f'{owner}: {code} {original} (content-type {content_type or "missing"}; expected {expected.content_types})', None
    err = api_error(body[:200000])
    if err and not (templated and host(url) in {'api.e-stat.go.jp', 'api.calil.jp'}):
        return 'FAIL', f'{owner}: {code} {original} (API-level error: {err})', None
    return 'OK', f'{owner}: {code} {content_type} {original} [{expected.label}]', None

def main():
    items = collect_urls()
    warn_counts = {key: 0 for key in WARN_RULES}
    failed = False
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(check, item) for item in items.items()]
        for future in as_completed(futures):
            status, message, reason = future.result()
            print(f'{status:5} {message}')
            failed |= status == 'FAIL'
            if reason:
                warn_counts[reason] += 1
    for reason, rule in WARN_RULES.items():
        count = warn_counts[reason]
        if TODAY > rule.expires:
            print(f'FAIL  WARN rule {reason} expired on {rule.expires}')
            failed = True
        elif count > rule.budget:
            print(f'FAIL  WARN rule {reason} used {count}/{rule.budget} budget')
            failed = True
        else:
            print(f'OK    WARN rule {reason}: {count}/{rule.budget}, expires {rule.expires}')
    print(f'Checked {len(items)} unique URLs from README.md, */SKILL.md, and docs/**/*.md')
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
