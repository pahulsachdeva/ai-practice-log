import unittest
import subprocess
import sys
from pathlib import Path
from datetime import date

from task_history import format_history, task_history


def entry(day, task='Make a quiz', result='with help'):
    return {'date': day, 'task': task, 'result': result, 'note': 'Try fewer questions.'}


class TaskHistoryTests(unittest.TestCase):
    def test_whole_task_name_matches_without_case_or_extra_spaces(self):
        rows = [entry('2026-10-01'), entry('2026-10-02', 'Make a quiz for biology')]
        self.assertEqual(task_history(rows, ' MAKE   a QUIZ '), [rows[0]])
        self.assertEqual(task_history(rows, 'quiz'), [])

    def test_dates_include_both_endpoints_and_leave_input_unchanged(self):
        rows = [entry('2026-10-03'), entry('2026-10-01'), entry('2026-10-02')]
        before = list(rows)
        found = task_history(rows, 'Make a quiz', date(2026, 10, 1), date(2026, 10, 2))
        self.assertEqual([row['date'] for row in found], ['2026-10-01', '2026-10-02'])
        self.assertEqual(rows, before)
        self.assertEqual(len(task_history(rows, 'Make a quiz', end=date(2026, 10, 1))), 1)

    def test_same_day_entries_keep_their_original_order(self):
        rows = [entry('2026-10-01', result='not yet'), entry('2026-10-01', result='on my own')]
        self.assertEqual(task_history(rows, 'Make a quiz'), rows)

    def test_a_setback_stays_visible(self):
        rows = [entry('2026-10-01', result='on my own'), entry('2026-10-02', result='with help')]
        text = format_history(task_history(rows, 'Make a quiz'))
        self.assertIn('2026-10-01 | on my own', text)
        self.assertIn('2026-10-02 | with help', text)
        self.assertIn('go back and forth', text)

    def test_bad_range_and_blank_task_have_clear_errors(self):
        with self.assertRaisesRegex(ValueError, 'start date'):
            task_history([], 'Quiz', date(2026, 10, 2), date(2026, 10, 1))
        with self.assertRaisesRegex(ValueError, 'task name'):
            task_history([], '  ')
        self.assertIn('No entries', format_history([]))


class HistoryCommandTests(unittest.TestCase):
    def test_command_reports_bad_date_range_without_a_traceback(self):
        folder = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, 'task_history.py', 'Make a quiz',
                                 '--start', '2026-10-05', '--end', '2026-10-01'],
                                cwd=folder, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('start date', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_example_command_keeps_the_source_file_unchanged(self):
        folder = Path(__file__).resolve().parents[1]
        source = folder / 'examples' / 'practice.csv'
        before = source.read_bytes()
        result = subprocess.run([sys.executable, 'task_history.py',
                                 'Turn notes into a study quiz', '--file', str(source)],
                                cwd=folder, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Practice sessions: 2', result.stdout)
        self.assertEqual(source.read_bytes(), before)
