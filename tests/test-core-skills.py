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
