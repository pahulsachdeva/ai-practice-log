# Make a weekly practice report

This command turns the CSV into a small text report. It counts sessions, days practised, different tasks, and results for one week.

## Try it

```bash
python3 practice_report.py --file examples/practice.csv --week 2026-10-01
```

Any date in the week works. This example covers September 28 through October 4. There are four sessions on four days and three different tasks.

To save a copy:

```bash
python3 practice_report.py --file examples/practice.csv --week 2026-10-01 --output example-week.txt
```

The command refuses to replace an existing file. Pick a new filename if you want another copy. Without `--output`, it just prints the report. Without `--file` or `--week`, it uses your personal CSV and the current week.

## What the counts mean

A week starts on Monday. For the current week, the report stops at today. Future entries do not count.

Every attempt counts as a session. Several attempts on one date count as one day practised. Task names ignore capital letters and extra spaces. Free-text notes stay out of the report.

The report helps review practice habits. More sessions do not by themselves mean someone learned more or that an AI product worked better.

## Python to work through

- Importing functions from another Python file.
- A loop to keep entries inside a date range.
- A `set` to count different dates and task names.
- `Counter` to count the three results.
- Joining a list of lines into text.
- Opening a file with `x` so an old file is not replaced.

Run the checks with `python3 -m unittest discover -s tests -v`.
