import tempfile
import unittest
import subprocess
import sys
from datetime import date
from pathlib import Path

from practice_report import make_report, save_report


def entry(day, task='Make a quiz', result='with help'):
    return {'date': day, 'task': task, 'result': result, 'note': 'A private note.'}


class PracticeReportTests(unittest.TestCase):
    def test_sessions_days_and_tasks_count_different_things(self):
        rows = [entry('2026-10-01'), entry('2026-10-01', ' MAKE   a QUIZ '),
                entry('2026-10-02', 'Rewrite an email', 'on my own')]
        text = make_report(rows, date(2026, 10, 1), date(2026, 10, 4))
        self.assertIn('Sessions logged: 3', text)
        self.assertIn('Days practised: 2', text)
        self.assertIn('Different tasks: 2', text)
        self.assertIn('With help: 2', text)
        self.assertNotIn('A private note.', text)

    def test_week_crosses_year_and_includes_monday_and_sunday(self):
        rows = [entry(day) for day in ['2025-12-28', '2025-12-29', '2026-01-04', '2026-01-05']]
        text = make_report(rows, date(2026, 1, 1), date(2026, 1, 10))
        self.assertIn('Week starting: 2025-12-29', text)
        self.assertIn('Entries included through: 2026-01-04', text)
        self.assertIn('Sessions logged: 2', text)

    def test_current_week_does_not_count_future_entries(self):
        rows = [entry('2026-10-01'), entry('2026-10-04')]
        text = make_report(rows, date(2026, 10, 1), date(2026, 10, 1))
        self.assertIn('Sessions logged: 1', text)
        self.assertIn('Entries included through: 2026-10-01', text)
        with self.assertRaisesRegex(ValueError, 'earlier week'):
            make_report([], date(2026, 10, 12), date(2026, 10, 1))

    def test_empty_week_is_explained(self):
        text = make_report([], date(2026, 10, 1), date(2026, 10, 4))
        self.assertIn('Sessions logged: 0', text)
        self.assertIn('No practice entries', text)

    def test_save_creates_a_file_and_never_overwrites_an_old_one(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'report.txt'
            save_report(path, 'First report')
            with self.assertRaises(FileExistsError):
                save_report(path, 'Replacement')
            self.assertEqual(path.read_text(), 'First report')


class ReportCommandTests(unittest.TestCase):
    def test_output_cannot_overwrite_the_input_csv(self):
        folder = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'practice.csv'
            source.write_bytes((folder / 'examples' / 'practice.csv').read_bytes())
            before = source.read_bytes()
            result = subprocess.run([sys.executable, 'practice_report.py', '--file', str(source),
                                     '--week', '2026-10-01', '--output', str(source)],
                                    cwd=folder, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('Traceback', result.stderr)
            self.assertEqual(source.read_bytes(), before)

    def test_example_command_prints_expected_counts(self):
        folder = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, 'practice_report.py',
                                 '--file', 'examples/practice.csv', '--week', '2026-10-01'],
                                cwd=folder, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Sessions logged: 4', result.stdout)
        self.assertIn('Days practised: 4', result.stdout)
