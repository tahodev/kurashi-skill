import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "lookup.py"
SPEC = importlib.util.spec_from_file_location("shelter_lookup", MODULE_PATH)
lookup = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(lookup)


class ShelterLookupTests(unittest.TestCase):
    def test_haversine_known_distance(self):
        # One degree of longitude at the equator is about 111.2 km.
        self.assertAlmostEqual(lookup.haversine_km(0, 0, 0, 1), 111.195, places=3)

    def test_filters_hazard_sorts_and_limits(self):
        headers = ["施設・場所名", "洪水", "地震", "緯度", "経度"]
        rows = [
            ["far", "1", "", "35.1", "139"],
            ["wrong hazard", "", "1", "35.001", "139"],
            ["near", "1", "", "35.01", "139"],
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sites.csv"
            with path.open("w", encoding="utf-8-sig", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(headers)
                writer.writerows(rows)
            results = lookup.nearest_sites(path, 35, 139, "洪水", 1)
        self.assertEqual(results[0][1]["施設・場所名"], "near")


if __name__ == "__main__":
    unittest.main()
