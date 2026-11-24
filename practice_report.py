"""Write a short weekly report from the practice CSV."""

import argparse
import csv
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from practice_log import LOG_FILE, RESULTS, read_sessions


def sessions_between(sessions, start, end):
    rows = []
    for session in sessions:
        day = date.fromisoformat(session['date'])
        if start <= day <= end:
            rows.append(session)
    return rows


def activity_counts(rows):
    # A set keeps each date once, even if several sessions happened that day.
    days = {date.fromisoformat(row['date']) for row in rows}
    tasks = {' '.join(row['task'].split()).casefold() for row in rows}
    return {'Sessions logged': len(rows),
            'Days practised': len(days),
            'Different tasks': len(tasks)}


def make_report(sessions, week, today=None, *, compare=False):
    today = today or date.today()
    # Any date in the week works. Move back to its Monday first.
    monday = week - timedelta(days=week.weekday())
    if monday > today:
        raise ValueError('Choose this week or an earlier week.')
    # This week may still be in progress, so do not include future dates.
    end = monday + timedelta(days=min(6, (today - monday).days))
    rows = sessions_between(sessions, monday, end)
    counts = Counter(row['result'] for row in rows)
    activity = activity_counts(rows)
    lines = ['AI Practice Log: weekly report',
             f'Week starting: {monday.isoformat()}',
             f'Entries included through: {end.isoformat()}', '']
    lines.extend(f'{label}: {count}' for label, count in activity.items())
    lines.append('')
    for result in RESULTS:
        lines.append(f'{result.capitalize()}: {counts[result]}')
    if not rows:
        lines.extend(['', 'No practice entries in this date range.'])
    if compare:
        # Shift both ends so a partial week compares the same weekdays.
        if (monday - date.min).days < 7:
            raise ValueError('The selected week has no earlier calendar week to compare.')
        previous_start = monday - timedelta(days=7)
        previous_end = end - timedelta(days=7)
        previous = activity_counts(sessions_between(sessions, previous_start, previous_end))
        lines.extend(['', f'Previous period: {previous_start.isoformat()} to {previous_end.isoformat()}'])
        for label, count in activity.items():
            change = count - previous[label]
            lines.append(f'{label}: {previous[label]} to {count} ({change:+d})')
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
    parser.add_argument('--compare', action='store_true',
                        help='compare with the same weekdays in the previous week')
    parser.add_argument('--output', type=Path, help='save to a new text file')
    args = parser.parse_args()
    try:
        text = make_report(read_sessions(args.file), args.week, compare=args.compare)
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
