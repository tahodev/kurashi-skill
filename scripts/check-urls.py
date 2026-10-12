#!/usr/bin/env python3
"""Check every documented URL against explicit response and WARN contracts."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import json
from urllib.parse import quote, urljoin
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
    (re.compile(r'^https://kokkai\.ndl\.go\.jp/api/'), Contract((200, 400), ('application/json', 'application/xml', 'text/xml', 'text/html'), 'Kokkai API')),
    (re.compile(r'^https://laws\.e-gov\.go\.jp/api/2/swagger-ui/'), Contract((200,), ('text/html',), 'e-Gov Law API v2 Swagger UI')),
    (re.compile(r'^https://(laws|elaws)\.e-gov\.go\.jp/api/'), Contract((200, 301, 400), ('application/json', 'application/xml', 'text/xml', 'text/html'), 'e-Gov Law API')),
    (re.compile(r'^https://www8\.cao\.go\.jp/chosei/shukujitsu/.+\.csv'), Contract((200,), ('text/csv', 'application/octet-stream', 'text/plain'), 'Cabinet Office CSV')),
    (re.compile(r'^https://www\.post\.japanpost\.jp/.+\.zip'), Contract((200,), ('application/zip', 'application/octet-stream'), 'Japan Post ZIP')),
    (re.compile(r'^https://www\.aozora\.gr\.jp/index_pages/.+\.zip'), Contract((200,), ('application/zip',), 'Aozora ZIP')),
    (re.compile(r'^https://maps\.gsi\.go\.jp/js/muni\.js$'), Contract((200,), ('text/javascript', 'application/javascript'), 'GSI muni.js')),
    (re.compile(r'^https://raw\.githubusercontent\.com/.+\.csv'), Contract((200,), ('text/plain', 'text/csv'), 'GitHub raw CSV')),
    (re.compile(r'^https://soramame\.env\.go\.jp/data/sokutei/.+\.csv'), Contract((200,), ('text/csv', 'application/octet-stream', 'text/plain'), 'AEROS CSV')),
    (re.compile(r'^https://soramame\.env\.go\.jp/'), Contract((200,), ('application/json', 'text/csv', 'text/plain', 'application/octet-stream'), 'AEROS API')),
    (re.compile(r'^https://www\.wbgt\.env\.go\.jp/api/v1/'), Contract((200,), ('application/json',), 'WBGT API v1')),
    (re.compile(r'^https://www\.wbgt\.env\.go\.jp/man15NH/'), Contract((200,), ('text/csv', 'application/pdf', 'application/octet-stream', 'text/plain'), 'WBGT master/manual')),
    (re.compile(r'^https://dataset\.address-br\.digital\.go\.jp/api/'), Contract((200,), ('application/json', 'application/geo+json'), 'ABR Hub API')),
    (re.compile(r'^https://data\.address-br\.digital\.go\.jp/.+\.zip'), Contract((200,), ('application/zip', 'application/octet-stream'), 'ABR ZIP')),
]
DEFAULT_CONTRACT = Contract(tuple(range(200, 400)), ('text/html', 'text/plain', 'text/csv', 'text/xml', 'application/xml', 'application/rss', 'application/pdf', 'application/json', 'application/octet-stream', 'image/'), 'documentation page')

# A WARN is temporary debt, never an open-ended host allowlist. Budgets are per reason.
WARN_RULES = {
    'ci-geo-network': WarnRule('GitHub-hosted runners may be blocked by Japanese public sites', date(2026, 12, 31), 15),
    'ken-all-datacenter': WarnRule('ZIP link is present on the official page but download returns 403/404 from this network; not verified', date(2026, 12, 31), 1),
}
WARN_HOSTS = {
    'www.jma.go.jp', 'www8.cao.go.jp', 'www.soumu.go.jp', 'www.nta.go.jp',
    'www.bunka.go.jp', 'hinanmap.gsi.go.jp', 'www.kyoshin.bosai.go.jp',
    'eco.mtk.nao.ac.jp', 'www.post.japanpost.jp', 'www.e-stat.go.jp', 'api.e-stat.go.jp',
    'data.address-br.digital.go.jp', 'dataset.address-br.digital.go.jp',
    'soramame.env.go.jp', 'www.wbgt.env.go.jp',
}
QUIET_TIME_URLS = {'https://www.jma.go.jp/bosai/typhoon/data/list.json'}
EXCLUDE_URLS = {'https://www.jma.go.jp/bosai/quake/data/20260908234330_20260908234052_VXSE5k_1.json', 'https://www.wbgt.env.go.jp/prev15WG/dl/yohou_{yyyymmdd}.csv'}
URL_RE = re.compile(r'https?://[^\s)"`\'。，、；：（）<>]+')
PLACEHOLDERS = {
    'ESTAT_APP_ID': 'INVALID_CI_KEY', 'CALIL_APPKEY': 'INVALID_CI_KEY',
    'SESSION_ID': 'INVALID_CI_SESSION', 'href': 'utf/zip/utf_ken_all.zip',
    'BASE_DATE': date.today().strftime('%Y%m%d'),
    'z': '5', 'x': '28', 'y': '12',
    'PP': '13', 'person_id': '000148', 'work_id': '789',
    'SKT_CD': '13101010',
}

def resolve_amedas_time():
    """Resolve the live AMeDAS snapshot time so the map URL is checked against current data, not a dated 404."""
    try:
        out = subprocess.run(['curl', '-sS', '--max-time', '15', 'https://www.jma.go.jp/bosai/amedas/data/latest_time.txt'], capture_output=True, text=True, timeout=20).stdout.strip()
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', out)
        return ''.join(m.groups()) if m else None
    except Exception:
        return None

# Live probes: real data endpoints that no SKILL.md URL line exercises (a 400/HTML shell must not pass).
PROBES = [
    ('https://laws.e-gov.go.jp/api/2/laws?limit=1', 'total_count', 'e-Gov Law API v2 laws list'),
    ('https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?law_full_text_format=json&elm=Article%5B709%5D', 'law_info', 'e-Gov Law API v2 law_data (Civil Code, elm=Article[N])'),
    ('https://laws.e-gov.go.jp/api/2/keyword?keyword=%E6%AF%8D%E5%AD%90&limit=1', 'items', 'e-Gov Law API v2 keyword search'),
]

def probe(item):
    url, key, label = item
    try:
        proc = subprocess.run(['curl', '-sS', '-L', '--connect-timeout', '8', '--max-time', str(TIMEOUT), '-A', 'kurashi-skill-health-check/2.0', '-o', '-', '-w', '\n%{http_code}\n%{content_type}', url], capture_output=True, timeout=TIMEOUT + 5)
        output = proc.stdout.decode('utf-8', 'replace')
        body, _, tail = output.rpartition('\n')
        body, _, code = body.rpartition('\n')
    except subprocess.TimeoutExpired:
        return 'FAIL', f'probe timeout {url} [{label}]'
    code, tail = code.strip(), tail.strip().lower()
    if code == '200' and 'json' in tail and f'"{key}"' in body:
        return 'OK', f'probe 200 {tail} has "{key}" {url} [{label}]'
    return 'FAIL', f'probe {code} {tail} missing "{key}" {url} [{label}]'

def source_files():
    return [root / 'README.md', *root.glob('*/SKILL.md'), *[p for p in root.glob('docs/**/*.md') if 'archive' not in p.parts]]

def collect_urls():
    items = {}
    for path in source_files():
        for raw in URL_RE.findall(path.read_text(encoding='utf-8')):
            url = raw.rstrip('.,;。,)')
            items.setdefault(url, set()).add(str(path.relative_to(root)))
    return items

def materialize(url):
    def replace(match):
        key = match.group(1)
        return PLACEHOLDERS.get(key, match.group(0))
    url = re.sub(r'\$?\{([^{}]+)\}', replace, url)
    url = url.replace('SESSION_ID', PLACEHOLDERS['SESSION_ID'])
    return None if '{' in url or '}' in url else url


def curl_get(url):
    proc = subprocess.run(['curl', '-sS', '-L', '--connect-timeout', '8',
        '--max-time', str(TIMEOUT), '-A', 'kurashi-skill-health-check/3.0',
        '-o', '-', '-w', '\n%{http_code}\n%{content_type}', url],
        capture_output=True, timeout=TIMEOUT + 5)
    body, code, content_type = proc.stdout.rsplit(b'\n', 2)
    return body, code.decode().strip(), content_type.decode().strip().lower()


def resolve_live_parameters():
    """Never manufacture a radar time or a postal-download href."""
    errors = []
    try:
        body, code, _ = curl_get('https://www.jma.go.jp/bosai/jmatile/data/nowc/targetTimes_N1.json')
        times = json.loads(body)
        assert code == '200' and times and 'hrpns' in times[0]['elements']
        PLACEHOLDERS.update({k: times[0][k] for k in ('basetime', 'validtime')})
    except Exception as exc:
        errors.append(f'radar live timestamp unavailable: {exc}')
    try:
        body, code, _ = curl_get('https://www.post.japanpost.jp/zipcode/dl/utf-zip.html')
        match = re.search(r'utf/zip/utf_ken_all\.zip', body.decode('utf-8', 'replace'))
        assert code == '200' and match, 'download link not found in official page'
        PLACEHOLDERS['href'] = match.group(0)
    except Exception as exc:
        PLACEHOLDERS.pop('href', None)
        errors.append(f'KEN_ALL official download link unavailable: {exc}')
    now = datetime.now(timezone(timedelta(hours=9)))
    yesterday = now.date() - timedelta(days=1)
    hour = max((h for h in (5, 11, 17) if h <= now.hour), default=17)
    announce_date = now.date() if now.hour >= 5 else yesterday
    current = (now - timedelta(hours=2))
    PLACEHOLDERS.update({'YYYY': current.strftime('%Y'), 'MM': current.strftime('%m'),
        'DD': current.strftime('%d'), 'HH': current.strftime('%H'),
        'yyyymm': (now.replace(day=1) - timedelta(days=1)).strftime('%Y%m'), '01-47': '13', '項目': 'PM2_5,TEMP',
        '検索語': '東京都', 'yyyymmdd': yesterday.strftime('%Y%m%d')})
    try:
        body, code, _ = curl_get('https://soramame.env.go.jp/data/map/kyokuNoudo/metadata.json')
        latest = json.loads(body)['latest']
        match = re.fullmatch(r'(\d{4})/(\d{2})/(\d{2}) (\d{2}):\d{2}:\d{2}', latest)
        assert code == '200' and match, 'invalid AEROS latest timestamp'
        PLACEHOLDERS.update(dict(zip(('YYYY', 'MM', 'DD', 'HH'), match.groups())))
    except Exception as exc:
        errors.append(f'AEROS live timestamp unavailable: {exc}')
    dynamic = {
        'https://www.wbgt.env.go.jp/api/v1/getForecastData':
            '?location_type=1&date_search_type=3&wbgt_nos=44132&forecast_origin_date=' + announce_date.strftime('%Y%m%d') + f'{hour:02}0000',
        'https://www.wbgt.env.go.jp/api/v1/getSurveyData':
            '?data_type=0&data_type=1&location_type=1&wbgt_nos=44132&date_from=' + yesterday.strftime('%Y%m%d') + '000000&date_to=' + yesterday.strftime('%Y%m%d') + '235959',
    }
    return errors, dynamic


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
    patterns = [r'"status"\s*:\s*"error"', r'ERROR-[0-9]+', r'"(?:resultCode|returnCode)"\s*:\s*"?(?!00\b|INFO-000\b|0\b)([A-Z0-9_-]+)', r'<resultCode>\s*(?!00<)([^<]+)']
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
    if url and original in DYNAMIC_ENDPOINTS:
        url += DYNAMIC_ENDPOINTS[original]
    if url and '/soramame/api/data_search?' in url and 'End_YM=' not in url:
        url += '&End_YM=' + PLACEHOLDERS['yyyymm']
    if url and '/soramame/api/data_search?' in url and 'SKT_CD=' not in url:
        url += '&SKT_CD=13101010'
    if url:
        url = quote(url, safe=':/?&=%+-_.,')
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
        return 'OK', f'{owner}: 404 {original} (documented no-active-typhoon contract)', None
    if '/zipcode/dl/utf/zip/utf_ken_all.zip' in url and code in ('403', '404') and 'href' in PLACEHOLDERS:
        return warn('ken-all-datacenter', owner, code, original)
    if in_hosts(host(url), WARN_HOSTS) and code in ('403', '429') and re.search(r'access denied|forbidden|blocked|cloudfront|rate.limit', body, re.I):
        return warn('ci-geo-network', owner, code, original)
    if numeric not in expected.statuses:
        return 'FAIL', f'{owner}: {code} {original} (expected {expected.label} status {expected.statuses})', None
    # Empty-body 4xx probes can legitimately omit Content-Type; success responses cannot.
    if not content_type and 400 <= numeric < 500 and templated:
        pass
    elif not any(token in content_type for token in expected.content_types):
        return 'FAIL', f'{owner}: {code} {original} (content-type {content_type or "missing"}; expected {expected.content_types})', None
    if numeric == 200 and (original in DYNAMIC_ENDPOINTS or '/api/data_search' in url):
        try:
            data = json.loads(body)
            if not isinstance(data, (dict, list)):
                raise ValueError('not a JSON object/array')
            if original in DYNAMIC_ENDPOINTS and (data.get('status') != 'success' or not isinstance(data.get('data'), list)):
                raise ValueError('WBGT success/data contract missing')
        except (ValueError, AttributeError) as exc:
            return 'FAIL', f'{owner}: invalid API data {url}: {exc}', None
    if numeric == 200 and '/soramame/api/data_search?' in url:
        try:
            records = json.loads(body)
            if not isinstance(records, list) or (records and not {'SKT_CD', 'SKT_DATE', 'SKT_TIME'} <= records[0].keys()):
                raise ValueError('missing AEROS record keys')
        except (ValueError, AttributeError) as exc:
            return 'FAIL', f'{owner}: AEROS history contract {exc}', None
    if numeric == 200 and '/data/sokutei/' in url and url.endswith('.csv'):
        headers = {'/noudoAll/': '測定局コード', '/NoudoTime/': '年,月,日,時', '/pm25/': '都道府県コード'}
        for path, prefix in headers.items():
            if path in url and not body.lstrip('\ufeff').startswith(prefix):
                return 'FAIL', f'{owner}: CSV header missing {prefix}: {url}', None
    if numeric == 200 and '/api/search/v1/' in url:
        try:
            data = json.loads(body)
            if not isinstance(data.get('features'), list):
                raise ValueError('missing GeoJSON features')
        except (ValueError, AttributeError) as exc:
            return 'FAIL', f'{owner}: ABR GeoJSON contract {exc}', None
    if original in QUIET_TIME_URLS and numeric == 200:
        try:
            if not isinstance(json.loads(body), list):
                raise ValueError('expected array')
        except ValueError as exc:
            return 'FAIL', f'{owner}: typhoon payload {exc}', None
    err = api_error(body[:200000])
    if err and not (templated and host(url) in {'api.e-stat.go.jp', 'api.calil.jp'}):
        return 'FAIL', f'{owner}: {code} {original} (API-level error: {err})', None
    return 'OK', f'{owner}: {code} {content_type} {original} [{expected.label}]', None

DYNAMIC_ENDPOINTS = {}

def main():
    global DYNAMIC_ENDPOINTS
    resolution_errors, DYNAMIC_ENDPOINTS = resolve_live_parameters()
    for error in resolution_errors:
        print(f'FAIL  {error}')
    amedas_time = resolve_amedas_time()
    if amedas_time:
        PLACEHOLDERS['amedas_time'] = amedas_time
    items = collect_urls()
    warn_counts = {key: 0 for key in WARN_RULES}
    failed = bool(resolution_errors)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(check, item) for item in items.items()]
        for future in as_completed(futures):
            status, message, reason = future.result()
            print(f'{status:5} {message}')
            failed |= status == 'FAIL'
            if reason:
                warn_counts[reason] += 1
    for status, message in map(probe, PROBES):
        print(f'{status:5} {message}')
        failed |= status == 'FAIL'
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location('fare_check', root / 'scripts/check-yu-pack.py')
    fare_check = module_from_spec(spec)
    spec.loader.exec_module(fare_check)
    try:
        fare_check.check_live()
        print('OK    Yu-Pack official 49 fares and heavy surcharge match fixture')
    except Exception as exc:
        print(f'FAIL  Yu-Pack live semantic check: {exc}')
        failed = True
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
