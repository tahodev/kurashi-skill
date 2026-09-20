#!/usr/bin/env python3
"""Deterministic smoke/regression tests for the five original core skills."""
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
