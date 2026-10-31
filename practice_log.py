"""Keep a small record of tasks practised with an AI assistant."""

import csv
import json
import os
import tempfile
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

LOG_FILE = Path(__file__).parent / 'practice.csv'
GOAL_FILE = LOG_FILE.with_name('goal.json')
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


def search_sessions(sessions, query):
    query = query.strip().casefold()
    return [session for session in sessions
            if query in (session['task'] + ' ' + session['note']).casefold()]


def weekly_progress(sessions, today=None):
    today = today or date.today()
    monday = today - timedelta(days=today.weekday())
    return sum(monday <= date.fromisoformat(session['date']) <= today
               for session in sessions)


def read_goal(path):
    if not path.exists():
        return 3
    with path.open(encoding='utf-8') as file:
        goal = json.load(file)
    if type(goal) is not int or not 1 <= goal <= 100:
        raise ValueError('The weekly goal must be a whole number from 1 to 100.')
    return goal


def save_goal(path, goal):
    if type(goal) is not int or not 1 <= goal <= 100:
        raise ValueError('Choose a whole number from 1 to 100.')
    path.write_text(json.dumps(goal) + '\n', encoding='utf-8')


def edit_session(path, entry_number, task, result, note):
    sessions = read_sessions(path)
    if not 1 <= entry_number <= len(sessions):
        raise ValueError('Choose one of the entry numbers shown.')
    if not task.strip() or result not in RESULTS:
        raise ValueError('Add a task and choose a valid result.')
    old = sessions[entry_number - 1]
    sessions[entry_number - 1] = {**old, 'task': task.strip(),
                                  'result': result, 'note': note.strip()}
    # Write a new file first. Replace the original only after writing succeeds.
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8',
                                         dir=path.parent, delete=False) as file:
            temp_path = Path(file.name)
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(sessions)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def show_weekly_goal():
    goal = read_goal(GOAL_FILE)
    completed = weekly_progress(read_sessions(LOG_FILE))
    print(f'This week: {completed} of {goal} practice sessions (Monday to today).')
    if completed >= goal:
        print('You reached your goal for this week.')
    else:
        print(f'{goal - completed} more to reach your goal.')
    choice = input('New weekly goal, or press Enter to keep it: ').strip()
    if choice:
        save_goal(GOAL_FILE, int(choice))
        print('Weekly goal saved.')


def edit_entry():
    sessions = read_sessions(LOG_FILE)
    if not sessions:
        print('No entries to edit yet.')
        return
    for number, session in enumerate(sessions, start=1):
        print(f"{number}. {session['date']} | {session['task']} | {session['result']}")
    entry_number = int(input('Which entry should change? '))
    if not 1 <= entry_number <= len(sessions):
        raise ValueError('Choose one of the entry numbers shown.')
    old = sessions[entry_number - 1]
    task = input(f"Task [{old['task']}]: ").strip() or old['task']
    for number, result in enumerate(RESULTS, start=1):
        print(f'{number}. {result.capitalize()}')
    choice = input(f"Result [{old['result']}], or choose 1, 2, or 3: ").strip()
    if choice and choice not in ['1', '2', '3']:
        raise ValueError('Choose 1, 2, or 3. No changes were saved.')
    result = RESULTS[int(choice) - 1] if choice else old['result']
    note = input('Note (Enter to keep it, - to clear it): ')
    note = '' if note == '-' else note or old['note']
    edit_session(LOG_FILE, entry_number, task, result, note)
    print('Entry updated. Its original date was kept.')


def main():
    print('AI Practice Log')
    while True:
        print('\n1. Add practice\n2. See summary\n3. Read past notes'
              '\n4. Search notes\n5. Weekly goal\n6. Edit an entry\n7. Exit')
        try:
            choice = input('Choose an option: ').strip()
            if choice == '1':
                add_session()
            elif choice == '2':
                show_summary(read_sessions(LOG_FILE))
            elif choice == '3':
                show_history(read_sessions(LOG_FILE))
            elif choice == '4':
                query = input('Search task names and notes: ').strip()
                matches = search_sessions(read_sessions(LOG_FILE), query)
                if matches:
                    show_history(matches)
                else:
                    print('No matching entries. Try a different word.')
            elif choice == '5':
                show_weekly_goal()
            elif choice == '6':
                edit_entry()
            elif choice == '7':
                print('See you next time.')
                break
            else:
                print('Choose a number from 1 to 7.')
        except (ValueError, OSError, csv.Error) as error:
            print(f'Could not finish: {error}')
        except (EOFError, KeyboardInterrupt):
            print('\nSee you next time.')
            break


if __name__ == '__main__':
    main()
