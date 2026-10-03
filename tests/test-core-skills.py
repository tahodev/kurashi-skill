#!/usr/bin/env python3
"""Deterministic smoke/regression tests with fixed fixtures (core + recent API skills)."""
from datetime import datetime
from pathlib import Path
import csv, io, json

fixtures = Path(__file__).parent / 'fixtures'
checks = []

def smoke(name):
    def decorate(fn):
        checks.append((name, fn))
        return fn
    return decorate

@smoke('jma-weather')
def check_weather():
    data = json.loads((fixtures / 'jma-weather.json').read_text())
    assert datetime.fromisoformat(data[0]['reportDatetime']).utcoffset() is not None
    assert data[0]['timeSeries'][0]['areas'][0]['weathers'] == ['晴れ', 'くもり']

@smoke('bosai-alert')
def check_bosai():
    data = json.loads((fixtures / 'bosai-alert.json').read_text())
    assert data[0]['ttl'] == '震源・震度に関する情報'
    assert data[0]['json'].endswith('.json')

@smoke('japan-holidays')
def check_holidays():
    rows = list(csv.DictReader(io.StringIO((fixtures / 'japan-holidays.csv').read_text())))
    assert rows[1] == {'国民の祝日・休日月日': '2026/01/12', '国民の祝日・休日名称': '成人の日'}

@smoke('furusato-nozei')
def check_furusato():
    case = json.loads((fixtures / 'furusato-nozei.json').read_text())
    # SKILL.md formula: levy*20%/(90%-income-tax-rate*1.021)+2,000.
    actual = round(case['resident_tax_income_levy'] * .20 / (.90 - case['income_tax_rate'] * 1.021) + 2000)
    assert actual == case['expected_cap_yen'], (actual, case['expected_cap_yen'])

@smoke('calil-books')
def check_calil():
    data = json.loads((fixtures / 'calil-books.json').read_text())
    assert data['continue'] == 0
    assert data['books']['9784478025819']['Tokyo_Setagaya']['libkey']['中央'] == '貸出可'


@smoke('volcano')
def check_volcano():
    warns = json.loads((fixtures / 'volcano-warning.json').read_text())
    master = {v['code']: v for v in json.loads((fixtures / 'volcano-list.json').read_text())}
    ioto = [w for w in warns if master[w['eventId']]['name_jp'] == '硫黄島'][0]
    # 未解除の警報は残り続ける: 2007年のエントリが現存するので reportDatetime を必ず引用する
    assert ioto['reportDatetime'].startswith('2007-12-01')
    levels = [it['name'] for w in warns for vi in w['volcanoInfos'] for it in vi['items']]
    assert 'レベル３（入山規制）' in levels

@smoke('amedas-weather')
def check_amedas():
    stations = json.loads((fixtures / 'amedas-stations.json').read_text())
    obs = json.loads((fixtures / 'amedas-map.json').read_text())
    tokyo = obs['44132']
    assert stations['44132']['type'] == 'A' and stations['44132']['kjName'] == '東京'
    assert tokyo['temp'][0] == 23.1 and tokyo['pressure'][0] == 1013.0
    # type C 観測所は気圧・湿度を持たない(要素は観測所タイプで違う)
    assert 'pressure' not in obs['11001']

@smoke('air-quality')
def check_air_quality():
    rows = list(csv.reader(io.StringIO((fixtures / 'air-quality-noudoall.csv').read_text())))
    hdr, data = rows[0], rows[1:]
    assert hdr[0] == '測定局コード' and hdr[11] == 'PM2.5'
    # '-' は未測定。推測で埋めない
    assert data[2][11] == '-'

@smoke('garbage-day')
def check_garbage_day():
    rows = list(csv.DictReader(io.StringIO((fixtures / 'garbage-day-area.csv').read_text())))
    assert rows[0]['燃やすごみ'] == '月 木' and rows[0]['燃やさないごみ'] == '水4'
    target = list(csv.DictReader(io.StringIO((fixtures / 'garbage-day-target.csv').read_text())))
    # ヘッダ名は自治体で違う(金沢は type)。引く前に1行目を読む
    assert list(target[0].keys()) == ['type', 'name', 'notice', 'furigana']
    assert target[1]['name'] == '乾電池(水銀)' and target[1]['notice'] == ''

@smoke('eew-monitor')
def check_eew():
    data = json.loads((fixtures / 'eew-jma.json').read_text())
    assert data['Issue']['Status'] == '通常' and data['isFinal'] is True
    # ペイロードには誤記 Magunitude が同居する。使うのは Magnitude
    assert data['Magnitude'] == 5.5

@smoke('estat-stats')
def check_estat():
    data = json.loads((fixtures / 'estat-statslist.json').read_text())
    # HTTP 200 でも応答JSONの STATUS を見る(100=認証失敗)
    assert data['GET_STATS_LIST']['RESULT']['STATUS'] == 0
    table = data['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF'][0]
    assert table['@id'] == '0000150002' and table['GOV_ORG']['$'] == '総務省'

@smoke('shelter-lookup')
def check_shelter():
    rows = list(csv.DictReader(io.StringIO((fixtures / 'shelter-merge.csv').read_text())))
    # 災害種別列は 1=指定。津波列(10列目)だけを見る
    tsunami = [r for r in rows if r['津波'] == '1']
    assert len(tsunami) == 1 and tsunami[0]['施設・場所名'] == '千代田区役所'
    assert rows[0]['住所'] == '千代田区九段南1-2-1'

import math, re
root = Path(__file__).parent.parent

def md_rows(skill, header_start):
    """Rows of the first Markdown table in SKILL.md whose header line starts with header_start."""
    lines = (root / skill / 'SKILL.md').read_text().split('\n')
    out, on = [], False
    for ln in lines:
        if ln.startswith(header_start):
            on = True
            continue
        if on:
            if not ln.startswith('|'):
                break
            if set(ln.replace('|', '').strip()) <= set('- '):
                continue
            out.append([c.strip() for c in ln.strip('|').split('|')])
    return out

@smoke('wareki')
def check_wareki():
    # SKILL.md の元号表を読み、境界日の変換を検証する(表そのものが正)
    eras = [(r[0], tuple(map(int, r[1].split('-')))) for r in md_rows('wareki', '| 元号')]
    eras.sort(key=lambda e: e[1])
    def to_wareki(y, m, d):
        name = [e for e in eras if e[1] <= (y, m, d)][-1]
        n = y - name[1][0] + 1
        return name[0], '元' if n == 1 else n
    assert to_wareki(1989, 1, 7) == ('昭和', 64)
    assert to_wareki(1989, 1, 8) == ('平成', '元')
    assert to_wareki(2019, 4, 30) == ('平成', 31)
    assert to_wareki(2019, 5, 1) == ('令和', '元')
    assert to_wareki(2026, 9, 11) == ('令和', 8)
    assert to_wareki(1912, 7, 30) == ('大正', '元')

@smoke('rokuyo')
def check_rokuyo():
    # SKILL.md の旧暦月テーブルを読み、(月+日)%6 の規則を検証する
    import datetime as dt
    rows = []
    pairs = [(r[i], r[i + 1]) for r in md_rows('rokuyo', '| 朔の日(新暦)') for i in (0, 2) if len(r) > i + 1]
    for a, b in pairs:
        if re.match(r'\d{4}-\d{2}-\d{2}$', a):
            rows.append((dt.date.fromisoformat(a), int(re.search(r'(\d+)月', b).group(1))))
    rows.sort()
    names = ['大安', '赤口', '先勝', '友引', '先負', '仏滅']
    def rokuyo(d):
        start, month = [r for r in rows if r[0] <= d][-1]
        return names[(month + (d - start).days + 1) % 6]
    assert rokuyo(dt.date(2026, 9, 11)) == '友引'   # SKILL.md の検証例(外部カレンダー照合済み)
    assert rokuyo(dt.date(2026, 9, 12)) == '先負'
    # 旧暦1日(朔)は月ごとに六曜が決まる: 1月・7月=先勝、2月・8月=友引、3月・9月=先負、4月・10月=仏滅、5月・11月=大安、6月・12月=赤口
    firsts = {1: '先勝', 2: '友引', 3: '先負', 4: '仏滅', 5: '大安', 6: '赤口'}
    for start, month in rows:
        if True:
            assert rokuyo(start) == firsts[(month - 1) % 6 + 1], (start, month)

@smoke('yubin-fee')
def check_yubin():
    rows = md_rows('yubin-fee', '| 重量')
    assert rows[0] == ['50g以内', '110円']
    extra = {r[0]: r[1:] for r in md_rows('yubin-fee', '| 重量 | 規格内')}
    # 定形外は重さが増えるほど料金が上がる。規格外は規格内より常に高い
    yen = lambda t: int(t.replace('円', '').replace(',', ''))
    ins = [yen(v[0]) for k, v in extra.items() if '対象外' not in v[0]]
    outs = [yen(v[1]) for v in extra.values()]
    assert ins == sorted(ins) and outs == sorted(outs)
    assert all(yen(v[1]) > yen(v[0]) for v in extra.values() if '対象外' not in v[0])

@smoke('amagumo')
def check_amagumo():
    times = json.loads((fixtures / 'amagumo-targettimes-N1.json').read_text())
    # 各要素は basetime/validtime(YYYYMMDDHHMMSS, UTC)/elements。新しい順で返る
    for t in times:
        assert re.fullmatch(r'\d{14}', t['basetime']) and re.fullmatch(r'\d{14}', t['validtime'])
        assert 'hrpns' in t['elements']
    assert times[0]['validtime'] > times[1]['validtime']
    # SKILL.md のタイル座標式: 東京(35.68, 139.77) z=8 → 227,100
    lat, lon, z = 35.68, 139.77, 8
    n = 2 ** z
    x = int(n * ((lon + 180) / 360))
    y = int(n * (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2)
    assert (x, y) == (227, 100)

@smoke('bosai-typhoon')
def check_typhoon():
    # SKILL.md の判断規則: 404=台風なし(正常) / 200+配列=発生中 / それ以外=取得失敗(「なし」と言わない)
    def classify(status, body=None):
        if status == 404:
            return 'none'
        if status == 200 and isinstance(body, list):
            return 'active'
        return 'failed'
    assert classify(404) == 'none'
    assert classify(200, []) == 'active' and classify(200, [{}]) == 'active'
    assert classify(500) == 'failed' and classify(200, None) == 'failed' and classify(0) == 'failed'

@smoke('zipcode-lookup')
def check_zipcode():
    # 形式フィクスチャ(合成行): SKILL.md が説明する15列・全項目クォート・「以下に掲載がない場合」行・1郵便番号に複数行
    rows = list(csv.reader(io.StringIO((fixtures / 'zipcode-ken-all-format.csv').read_text())))
    assert all(len(r) == 15 for r in rows)
    assert all(re.fullmatch(r'\d{7}', r[2]) for r in rows)
    same = [r for r in rows if r[2] == '9999991']
    assert len(same) == 2, 'one postal code can map to several rows'
    assert [r for r in rows if r[8] == '以下に掲載がない場合']

failed = 0
for name, check in checks:
    try:
        check()
        print(f'OK    {name} fixture smoke test')
    except Exception as exc:
        failed += 1
        print(f'FAIL  {name}: {exc}')
print(f'Checked {len(checks)} core skill smoke tests with fixed fixtures')
raise SystemExit(1 if failed else 0)
