"""Negative controls check intended rejection reasons, without real secrets."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate import ROOT as SOURCE, REPO_FILES, ValidationError, validate_tree, validate_archive
from build_release import build


class PackageControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='practical-work-kit-test-')
        self.case = Path(self.temp.name).resolve()
        self.root = self.case / 'repo'
        self.root.mkdir()
        for rel in REPO_FILES:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / rel, target)

    def tearDown(self):
        # Only remove the TemporaryDirectory created by this test; never a user repo.
        self.assertTrue(self.root.resolve().is_relative_to(self.case))
        self.temp.cleanup()

    def test_clean_source_and_archive(self):
        self.assertEqual(validate_tree(self.root)['status'], 'PASS')
        result = build(self.root / 'dist', self.root)
        self.assertEqual(result['status'], 'PASS')
        first = (self.root / 'dist' / result['archive']).read_bytes()
        build(self.root / 'dist', self.root)
        self.assertEqual(first, (self.root / 'dist' / result['archive']).read_bytes())

    def test_secret_rejected_by_real_cli(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n' + 'ghp_' + 'A' * 40, encoding='utf-8')
        process = subprocess.run([sys.executable, str(SOURCE / 'tools/validate.py'), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(process.returncode, 1)
        report = json.loads(process.stdout)
        self.assertEqual(report['status'], 'FAIL')
        self.assertTrue(report['reason'].startswith('github_token:README.md:'))
        self.assertNotIn('A' * 40, process.stdout)

    def test_extra_private_file_rejected(self):
        (self.root / 'private-notes.txt').write_text('must stay out', encoding='utf-8')
        with self.assertRaisesRegex(ValidationError, '^public_file_set$'):
            validate_tree(self.root)

    def test_tracked_ignored_file_rejected(self):
        private = self.root / '.venv/private-notes.txt'
        private.parent.mkdir()
        private.write_text('ghp_' + 'A' * 40, encoding='utf-8')
        # Ordinary untracked caches are harmless to the Git publication set.
        self.assertEqual(validate_tree(self.root)['status'], 'PASS')
        empty_template = self.case / 'empty-template'
        empty_template.mkdir()
        subprocess.run(['git', 'init', '--initial-branch=main', '--template=' + str(empty_template), str(self.root)], capture_output=True, check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', '--', '.venv/private-notes.txt'], capture_output=True, check=True)
        with self.assertRaisesRegex(ValidationError, '^tracked_private_or_extra_file$'):
            validate_tree(self.root)

    def test_hardlinked_outputs_do_not_modify_outside_files(self):
        output = self.root / 'dist'
        output.mkdir()
        for name in ['practical-work-kit-0.1.0.zip', 'SHA256SUMS.txt']:
            sentinel = self.case / ('outside-' + name)
            sentinel.write_bytes(b'isolated sentinel')
            (output / name).hardlink_to(sentinel)
        result = build(output, self.root)
        self.assertEqual(result['status'], 'PASS')
        for name in ['practical-work-kit-0.1.0.zip', 'SHA256SUMS.txt']:
            self.assertEqual((self.case / ('outside-' + name)).read_bytes(), b'isolated sentinel')
            self.assertNotEqual((output / name).read_bytes(), b'isolated sentinel')

    def test_private_path_rejected(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text(encoding='utf-8') + '\nC:/' + 'Users/fictional/private-note.txt', encoding='utf-8')
        with self.assertRaisesRegex(ValidationError, '^private_home_path:'):
            validate_tree(self.root)

    def test_duplicate_json_key_rejected(self):
        (self.root / 'plugin.json').write_text('{"name":"one","name":"two"}', encoding='utf-8')
        with self.assertRaisesRegex(ValidationError, '^duplicate_json_key$'):
            validate_tree(self.root)

    def test_missing_reference_rejected(self):
        path = self.root / 'skills/check-my-work/SKILL.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n[missing](references/missing.md)', encoding='utf-8')
        with self.assertRaisesRegex(ValidationError, '^missing_or_unsafe_reference:'):
            validate_tree(self.root)

    def test_license_tamper_rejected(self):
        (self.root / 'licenses/Pablo-aps__prove-it.txt').write_text('changed license', encoding='utf-8')
        with self.assertRaisesRegex(ValidationError, '^license_hash:'):
            validate_tree(self.root)

    def test_archive_traversal_rejected(self):
        archive = self.case / 'attack.zip'
        with zipfile.ZipFile(archive, 'w') as bundle:
            bundle.writestr('../escape.txt', 'never extract')
        with self.assertRaisesRegex(ValidationError, '^archive_path$'):
            validate_archive(archive, self.root)

    def test_archive_content_tamper_rejected(self):
        result = build(self.root / 'dist', self.root)
        original = self.root / 'dist' / result['archive']
        changed = self.case / 'changed.zip'
        with zipfile.ZipFile(original) as good, zipfile.ZipFile(changed, 'w') as bad:
            for item in good.infolist():
                bad.writestr(item, b'changed' if item.filename == 'plugin.json' else good.read(item))
        with self.assertRaisesRegex(ValidationError, '^archive_content$'):
            validate_archive(changed, self.root)


if __name__ == '__main__':
    unittest.main()
