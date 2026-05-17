import tempfile
import unittest
from pathlib import Path

from scripts.standard import standardctl


class StandardCtlTests(unittest.TestCase):
    def test_doctor_fails_without_lock(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'standard.yml').write_text('profile: ts-fullstack\n', encoding='utf-8')
            (root / 'apm.yml').write_text('packages: []\n', encoding='utf-8')
            rc = standardctl.doctor(root)
            self.assertEqual(rc, 1)

    def test_doctor_passes_with_minimum_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for p in ['standard.yml', 'apm.yml', 'apm.lock.yaml', '.copier-answers.yml']:
                (root / p).write_text('x: y\n', encoding='utf-8')
            (root / 'standard.yml').write_text('profile: ts-fullstack\n', encoding='utf-8')
            (root / 'apps/web').mkdir(parents=True)
            (root / 'apps/api').mkdir(parents=True)
            (root / 'packages/api-contract').mkdir(parents=True)
            rc = standardctl.doctor(root)
            self.assertEqual(rc, 0)

    def test_apply_writes_report(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            calls = []

            def fake(cmd, cwd):
                calls.append(cmd)
                return 0, 'ok'

            old = standardctl.run_cmd
            standardctl.run_cmd = fake
            try:
                rc = standardctl.apply_section(root, 'api-contract-openapi')
            finally:
                standardctl.run_cmd = old
            self.assertEqual(rc, 0)
            reports = list((root / 'docs/harness/adoptions').glob('*-api-contract-openapi.md'))
            self.assertTrue(reports)
            self.assertGreaterEqual(len(calls), 2)


if __name__ == '__main__':
    unittest.main()
