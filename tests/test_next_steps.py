import contextlib
import io
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import practice_log
from practice_log import (edit_session, read_goal, read_sessions, save_goal,
                          save_session, search_sessions, weekly_progress)


def entry(day, task='Make a quiz', note='Use shorter notes'):
    return {'date': day, 'task': task, 'result': 'with help', 'note': note}


class NextStepsTests(unittest.TestCase):
    def test_search_reads_tasks_and_notes_without_case_or_edge_spaces(self):
        sessions = [entry('2026-10-01'), entry('2026-10-02', 'Rewrite email', 'Keep my tone')]
        self.assertEqual(search_sessions(sessions, ' QUIZ '), [sessions[0]])
        self.assertEqual(search_sessions(sessions, 'TONE'), [sessions[1]])
        self.assertEqual(search_sessions(sessions, 'nothing'), [])
        self.assertEqual(search_sessions(sessions, ''), sessions)

    def test_week_starts_on_monday_and_ignores_future_entries(self):
        sessions = [entry(day) for day in ['2025-12-28', '2025-12-29', '2026-01-01', '2026-01-02']]
        self.assertEqual(weekly_progress(sessions, date(2026, 1, 1)), 2)
        self.assertEqual(weekly_progress(sessions, date(2025, 12, 29)), 1)
        self.assertEqual(weekly_progress([], date(2026, 1, 1)), 0)

    def test_goal_saves_and_rejects_invalid_numbers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'goal.json'
            self.assertEqual(read_goal(path), 3)
            save_goal(path, 5)
            self.assertEqual(read_goal(path), 5)
            for goal in [0, -1, 101, 2.5, True, '3']:
                with self.assertRaises(ValueError):
                    save_goal(path, goal)
                self.assertEqual(read_goal(path), 5)
            path.write_text('false')
            with self.assertRaises(ValueError):
                read_goal(path)

    def test_edit_keeps_date_and_other_entries_and_handles_csv_quotes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'practice.csv'
            save_session(path, 'Quiz', 'not yet')
            save_session(path, 'Email', 'on my own')
            before = read_sessions(path)
            edit_session(path, 1, 'Quiz', 'with help', 'Try "five questions", then check.\nRepeat.')
            after = read_sessions(path)
            self.assertEqual(after[0]['date'], before[0]['date'])
            self.assertEqual(after[0]['result'], 'with help')
            self.assertIn('\nRepeat.', after[0]['note'])
            self.assertEqual(after[1], before[1])
            original = path.read_bytes()
            for number in [0, 3]:
                with self.assertRaises(ValueError):
                    edit_session(path, number, 'Quiz', 'on my own', '')
                self.assertEqual(path.read_bytes(), original)

    def test_failed_edit_keeps_the_original_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'practice.csv'
            save_session(path, 'Quiz', 'not yet')
            original = path.read_bytes()
            with patch('practice_log.os.replace', side_effect=OSError('Could not save')):
                with self.assertRaises(OSError):
                    edit_session(path, 1, 'Quiz', 'on my own', '')
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_menu_can_add_search_edit_and_show_weekly_progress(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / 'practice.csv'
            goal = Path(folder) / 'goal.json'
            choices = ['1', 'Quiz', '3', 'Too broad', '4', 'broad',
                       '6', '1', '', '2', 'Try five questions', '5', '4', '7']
            output = io.StringIO()
            with patch.object(practice_log, 'LOG_FILE', log), patch.object(practice_log, 'GOAL_FILE', goal):
                with patch('builtins.input', side_effect=choices), contextlib.redirect_stdout(output):
                    practice_log.main()
            self.assertIn('Too broad', output.getvalue())
            self.assertIn('Entry updated.', output.getvalue())
            self.assertIn('This week: 1 of 3', output.getvalue())
            self.assertEqual(read_sessions(log)[0]['result'], 'with help')
            self.assertEqual(read_goal(goal), 4)


if __name__ == '__main__':
    unittest.main()
