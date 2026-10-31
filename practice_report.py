"""Write a short weekly report from the practice CSV."""

import argparse
import csv
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from practice_log import LOG_FILE, RESULTS, read_sessions


def make_report(sessions, week, today=None):
    today = today or date.today()
    # Any date in the week works. Move back to its Monday first.
    monday = week - timedelta(days=week.weekday())
    if monday > today:
        raise ValueError('Choose this week or an earlier week.')
    sunday = monday + timedelta(days=6)
    # This week may still be in progress, so do not include future dates.
    end = min(sunday, today)
    rows = []
    for session in sessions:
        day = date.fromisoformat(session['date'])
        if monday <= day <= end:
            rows.append(session)
    counts = Counter(row['result'] for row in rows)
    # A set keeps each date once, even if several sessions happened that day.
    days = {date.fromisoformat(row['date']) for row in rows}
    tasks = {' '.join(row['task'].split()).casefold() for row in rows}
    lines = ['AI Practice Log: weekly report',
             f'Week starting: {monday.isoformat()}',
             f'Entries included through: {end.isoformat()}', '',
             f'Sessions logged: {len(rows)}',
             f'Days practised: {len(days)}',
             f'Different tasks: {len(tasks)}', '']
    for result in RESULTS:
        lines.append(f'{result.capitalize()}: {counts[result]}')
    if not rows:
        lines.extend(['', 'No practice entries in this date range.'])
    lines.extend(['', 'Counts include every session, including repeat attempts.',
                  'These are personal practice notes, not a score for skill or AI accuracy.'])
    return '\n'.join(lines) + '\n'


def save_report(path, text):
    # x means create a new file. It refuses to replace a file that already exists.
    with path.open('x', encoding='utf-8') as file:
        file.write(text)


def main():
    parser = argparse.ArgumentParser(description='See a weekly AI practice report.')
    parser.add_argument('--file', type=Path, default=LOG_FILE, help='CSV to read')
    parser.add_argument('--week', type=date.fromisoformat, default=date.today(),
                        help='any date in the week, YYYY-MM-DD')
    parser.add_argument('--output', type=Path, help='save to a new text file')
    args = parser.parse_args()
    try:
        text = make_report(read_sessions(args.file), args.week)
        if args.output:
            save_report(args.output, text)
            print(f'Report saved to {args.output}')
        else:
            print(text, end='')
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(1, f'Could not make the report: {error}\n')


# Keep the functions available for tests without running the command.
if __name__ == '__main__':
    main()
