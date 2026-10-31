# Follow one task over time

The summary uses a task's latest result. This view keeps all its earlier attempts visible too. Needing help again is useful information, so it stays in the history.

## Try it

```bash
python3 task_history.py "Turn notes into a study quiz" --file examples/practice.csv
```

The example shows “not yet” on October 3 and “with help” on October 5. It shows the notes beside both entries.

To choose dates:

```bash
python3 task_history.py "Turn notes into a study quiz" --file examples/practice.csv --start 2026-10-01 --end 2026-10-04
```

Both dates are included. Leave either date out to keep that end open. Without `--file`, the program reads your personal `practice.csv`.

## Python to work through

- `argparse` reads options typed after the filename.
- `split()` and `join()` help match task names with extra spaces.
- A loop checks each entry against the name and dates.
- `sorted()` returns a new list without changing the original one.

Task names must match in full. Capital letters and extra spaces are ignored. Two entries on the same day keep their CSV order.

The result is a history of personal notes. It does not explain why a result changed or prove that a skill was learned.

Run the checks with `python3 -m unittest discover -s tests -v`.
