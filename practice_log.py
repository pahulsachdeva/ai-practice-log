"""Keep a small record of tasks practised with an AI assistant."""

import csv
from collections import Counter
from datetime import date
from pathlib import Path

LOG_FILE = Path(__file__).parent / 'practice.csv'
FIELDS = ['date', 'task', 'result', 'note']
RESULTS = ['on my own', 'with help', 'not yet']


def read_sessions(path):
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDS:
            raise ValueError('The CSV needs these columns: ' + ', '.join(FIELDS))
        sessions = list(reader)
    for row_number, session in enumerate(sessions, start=2):
        try:
            date.fromisoformat(session['date'])
            if not session['task'].strip() or session['result'] not in RESULTS:
                raise ValueError()
            if session['note'] is None or None in session:
                raise ValueError()
        except (ValueError, TypeError, AttributeError):
            raise ValueError(f'Check the date, task, and result on CSV row {row_number}.') from None
    return sessions


def save_session(path, task, result, note=''):
    task = task.strip()
    if not task:
        raise ValueError('Add a task name.')
    if result not in RESULTS:
        raise ValueError('Choose one of the three results.')
    # Check the old file before adding to it, so a broken CSV stays untouched.
    read_sessions(path)
    needs_header = not path.exists()
    with path.open('a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow({'date': date.today().isoformat(), 'task': task,
                         'result': result, 'note': note.strip()})


def show_summary(sessions):
    if not sessions:
        print('No practice logged yet. Add your first task.')
        return
    counts = Counter(session['result'] for session in sessions)
    print(f'\nPractice sessions: {len(sessions)}')
    for result in RESULTS:
        print(f'{result.capitalize()}: {counts[result]}')

    # For each task, use its latest dated entry. Later CSV rows break date ties.
    latest = {}
    for session in sorted(sessions, key=lambda row: date.fromisoformat(row['date'])):
        latest[session['task'].strip().casefold()] = session
    print('\nTasks to practise again:')
    tasks = [session for session in latest.values() if session['result'] != 'on my own']
    if not tasks:
        print('None from your latest entries. Try a new task when you are ready.')
    for session in tasks:
        print(f"- {session['task']} ({session['result']})")
    print('\nThese are your own notes, not a test of skill or AI accuracy.')


def show_history(sessions):
    if not sessions:
        print('No practice logged yet.')
    for session in sessions:
        print(f"\n{session['date']} | {session['task']} | {session['result']}")
        if session['note']:
            print('  ' + session['note'])


def add_session():
    task = input('What task did you try? ').strip()
    for number, result in enumerate(RESULTS, start=1):
        print(f'{number}. {result.capitalize()}')
    choice = input('How did it go? Choose 1, 2, or 3: ').strip()
    if choice not in ['1', '2', '3']:
        raise ValueError('Choose 1, 2, or 3. The session was not saved.')
    note = input('What would help next time? (optional): ')
    save_session(LOG_FILE, task, RESULTS[int(choice) - 1], note)
    print('Practice saved.')


def main():
    print('AI Practice Log')
    while True:
        print('\n1. Add practice\n2. See summary\n3. Read past notes\n4. Exit')
        try:
            choice = input('Choose an option: ').strip()
            if choice == '1':
                add_session()
            elif choice == '2':
                show_summary(read_sessions(LOG_FILE))
            elif choice == '3':
                show_history(read_sessions(LOG_FILE))
            elif choice == '4':
                print('See you next time.')
                break
            else:
                print('Choose 1, 2, 3, or 4.')
        except (ValueError, OSError) as error:
            print(f'Could not finish: {error}')
        except (EOFError, KeyboardInterrupt):
            print('\nSee you next time.')
            break


if __name__ == '__main__':
    main()
