#!/usr/bin/env python3
"""Verify all Tokyo-origin fares and heavy surcharge against official pages."""
from html.parser import HTMLParser
from pathlib import Path
import json, re, urllib.request
ROOT = Path(__file__).resolve().parents[1]


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.current, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.current = []
        elif tag == 'td' and self.current is not None:
            self.cell = ''

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.current.append(self.cell)
            self.cell = None
        elif tag == 'table' and self.current is not None:
            self.tables.append(self.current)
            self.current = None


def parse_fares(html):
    parser = Tables()
    parser.feed(html)
    rows = []
    for table in parser.tables:
        if len(table) == 14:
            sizes = [int(re.sub(r'\D', '', value)) for value in table[::2]]
            if sizes == [60, 80, 100, 120, 140, 160, 170]:
                rows.append([int(re.sub(r'\D', '', value)) for value in table[1::2]])
    if len(rows) != 7:
        raise ValueError(f'expected 7 destination regions, got {len(rows)}')
    return rows


def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'kurashi-skill-health-check/3.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f'official source returned {response.status}')
        return response.read().decode('utf-8')


def check_live():
    fixture = json.loads((ROOT / 'fixtures/yu-pack-2026-10.json').read_text())
    actual = parse_fares(get(fixture['source_url']))
    if actual != list(fixture['fares'].values()):
        raise ValueError('official fares changed: update SKILL.md and fixture, not just dates')
    heavy = get(fixture['heavy_source_url'])
    plain = re.sub('<[^>]+>', '', heavy)
    if not re.search(r'基本運賃\s*[＋+]\s*620\s*円', plain):
        raise ValueError('official heavy surcharge is not the documented 620 yen')


if __name__ == '__main__':
    check_live()
    print('OK all 49 Yu-Pack fares and heavy surcharge')
