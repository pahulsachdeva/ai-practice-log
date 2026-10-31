"""Read one task's practice entries in date order."""

import argparse
import csv
from datetime import date
from pathlib import Path

from practice_log import LOG_FILE, read_sessions


def task_key(name):
    # Split and join also remove extra spaces between words.
    return ' '.join(name.split()).casefold()


def task_history(sessions, task, start=None, end=None):
    if not task_key(task):
        raise ValueError('Enter a task name.')
    if start and end and start > end:
        raise ValueError('The start date must be on or before the end date.')
    matches = []
    for session in sessions:
        day = date.fromisoformat(session['date'])
        # Match the whole name so two different tasks do not get mixed together.
        if task_key(session['task']) != task_key(task):
            continue
        if start and day < start:
            continue
        if end and day > end:
            continue
        matches.append(session)
    # sorted() makes a new list. The original file order stays untouched.
    return sorted(matches, key=lambda session: date.fromisoformat(session['date']))


def format_history(sessions):
    if not sessions:
        return 'No entries found for that task and date range.'
    lines = [f"Task: {sessions[-1]['task'].strip()}", f'Practice sessions: {len(sessions)}', '']
    for session in sessions:
        lines.append(f"{session['date']} | {session['result']}")
        if session['note']:
            lines.append('  Note: ' + session['note'])
    lines.append('')
    lines.append('These entries show what was reported each time. Results can go back and forth.')
    return '\n'.join(lines)


def main():
    # argparse turns command-line options into values we can use in Python.
    parser = argparse.ArgumentParser(description='See one AI practice task over time.')
    parser.add_argument('task', help='the full task name, in quotes')
    parser.add_argument('--file', type=Path, default=LOG_FILE, help='CSV to read')
    parser.add_argument('--start', type=date.fromisoformat, help='first date, YYYY-MM-DD')
    parser.add_argument('--end', type=date.fromisoformat, help='last date, YYYY-MM-DD')
    args = parser.parse_args()
    try:
        sessions = read_sessions(args.file)
        matches = task_history(sessions, args.task, args.start, args.end)
        print(format_history(matches))
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(1, f'Could not read history: {error}\n')


# Importing these functions for a test should not start the program.
if __name__ == '__main__':
    main()
