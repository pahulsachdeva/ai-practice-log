import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from practice_log import read_sessions, save_session, show_summary


class PracticeLogTests(unittest.TestCase):
    def test_save_and_read_notes_with_commas_and_newlines(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'practice.csv'
            save_session(path, 'Write a quiz', 'with help', 'Try shorter notes, then check.\nAsk again.')
            session = read_sessions(path)[0]
            self.assertEqual(session['task'], 'Write a quiz')
            self.assertEqual(session['note'], 'Try shorter notes, then check.\nAsk again.')

    def test_latest_result_decides_what_to_practise(self):
        sessions = [
            {'date': '2026-10-02', 'task': 'Make a quiz', 'result': 'on my own', 'note': ''},
            {'date': '2026-10-01', 'task': ' make a QUIZ ', 'result': 'not yet', 'note': ''},
        ]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            show_summary(sessions)
        self.assertIn('Practice sessions: 2', output.getvalue())
        self.assertIn('None from your latest entries.', output.getvalue())

    def test_bad_input_does_not_change_the_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'practice.csv'
            save_session(path, 'Summarise notes', 'with help')
            original = path.read_text()
            for task, result in [(' ', 'on my own'), ('A task', 'maybe')]:
                with self.assertRaises(ValueError):
                    save_session(path, task, result)
                self.assertEqual(path.read_text(), original)

    def test_missing_file_is_empty_and_bad_csv_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'practice.csv'
            self.assertEqual(read_sessions(path), [])
            path.write_text('date,task,result,note\n2026-02-30,Quiz,not yet,\n')
            with self.assertRaisesRegex(ValueError, 'row 2'):
                read_sessions(path)


if __name__ == '__main__':
    unittest.main()
