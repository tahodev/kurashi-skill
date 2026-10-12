"""Regression tests for the checks, not just for skill fixtures."""
from datetime import date
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
import sys, unittest
ROOT = Path(__file__).resolve().parents[2]


def load(name, filename):
    spec = spec_from_file_location(name, ROOT / 'scripts' / filename)
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


static = load('static_check', 'check-static-data.py')
urls = load('url_check', 'check-urls.py')
fares = load('fare_check', 'check-yu-pack.py')
links = load('link_check', 'check-yaml-links.py')


class ExpiryTests(unittest.TestCase):
    def meta(self):
        return {'data_as_of': '2026-09-01', 'valid_through': '2027-09-01', 'effective_until': '2026-10-01'}

    def test_known_change_preempts_annual_review(self):
        self.assertFalse(static.expiry_errors(self.meta(), date(2026, 8, 30)))
        self.assertTrue(static.expiry_errors(self.meta(), date(2026, 9, 30)))
        self.assertIn('old data must not be used', ' '.join(static.expiry_errors(self.meta(), date(2026, 10, 1))))
        self.assertIn('old data must not be used', ' '.join(static.expiry_errors(self.meta(), date(2026, 10, 2))))

    def test_no_known_change_respects_review(self):
        meta = self.meta()
        del meta['effective_until']
        self.assertFalse(static.expiry_errors(meta, date(2026, 10, 13)))
        self.assertTrue(static.expiry_errors(meta, date(2027, 9, 2)))

    def test_invalid_change_order(self):
        meta = self.meta()
        meta['effective_until'] = meta['data_as_of']
        self.assertIn('effective_until must be after data_as_of', static.expiry_errors(meta, date(2026, 8, 1)))


class UrlTests(unittest.TestCase):
    def test_shell_placeholder_removes_dollar(self):
        urls.PLACEHOLDERS['href'] = 'utf/zip/utf_ken_all.zip'
        self.assertEqual(urls.materialize('https://example.invalid/${href}'), 'https://example.invalid/utf/zip/utf_ken_all.zip')

    def test_unknown_placeholder_not_probed(self):
        self.assertIsNone(urls.materialize('https://example.invalid/{missing}'))

    def test_typhoon_no_expiring_exception(self):
        self.assertNotIn('quiet-time-empty-feed', urls.WARN_RULES)
        self.assertIn('https://www.jma.go.jp/bosai/typhoon/data/list.json', urls.QUIET_TIME_URLS)

    def test_api_error_json(self):
        self.assertTrue(urls.api_error('{"status":"error","errMsg":[]}'))
        self.assertIsNone(urls.api_error('{"status":"success","data":[]}'))

    def test_wbgt_master_contract_unchanged(self):
        self.assertEqual(urls.contract_for('https://www.wbgt.env.go.jp/man15NH/wbgt_point_master-20260515.csv').label, 'WBGT master/manual')


class ParseTests(unittest.TestCase):
    def test_all_49_fares(self):
        import json
        f = json.loads((ROOT / 'fixtures/yu-pack-2026-10.json').read_text())
        markup = ''.join('<table>' + ''.join(f'<td>{size}サイズ</td><td>{value:,} 円</td>' for size, value in zip(f['sizes'], row)) + '</table>' for row in f['fares'].values())
        self.assertEqual(fares.parse_fares(markup), list(f['fares'].values()))

    def test_missing_region_rejected(self):
        with self.assertRaises(ValueError):
            fares.parse_fares('<table><td>60サイズ</td><td>840円</td></table>')

    def test_japanese_anchors(self):
        self.assertIn('料金表', links.anchors('# 料金表'))
        self.assertEqual(links.anchors('# A\n# A'), {'a', 'a-1'})
