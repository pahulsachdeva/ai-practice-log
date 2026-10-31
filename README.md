I studied neuroscience at Colgate University, but I also took Computer Science 101 and 102 and tried learning Python. I got through the courses, but I still feel like I can do much better.

I found JavaScript easier to get started with, especially when I could see what I was building on a screen. My other projects, [Sentient](https://github.com/pahulsachdeva/sentient-behavioral-intelligence) and [NeuroLift](https://github.com/pahulsachdeva/neurolift-behavioral-experiments), use JavaScript.

I now work for an AI company, and I want to understand more of the technical side. I'm coming back to Python and giving the basics more attention. This is the first Python project I'm sharing here. I kept it small so I can understand each part and build from there.

# AI Practice Log

A simple Python program to keep track of tasks I practise with an AI assistant.

Knowing about a feature and being able to use it on my own are two different things. I wanted a small place to record what I tried, how it went, and what I should practise again.

## What it does

- Saves a task, the date, how it went, and an optional note.
- Lets me choose **on my own**, **with help**, or **not yet**.
- Shows how many sessions I logged under each result.
- Lists tasks to practise again, based on the latest entry for each task.
- Keeps past notes in a CSV file I can open and read.
- Searches task names and notes.
- Tracks a weekly practice goal.
- Lets me correct an entry without changing its original date.

For example, I might practise asking an AI assistant to summarise an article or turn study notes into a quiz. The sample file has made-up entries like these. It has no work or customer data.

## Run it

Use Python 3.10 or later. There is nothing extra to install.

Download this repo, open a terminal in its folder, and run:

```bash
python3 practice_log.py
```

On Windows, you can use `py practice_log.py`.

```text
AI Practice Log

1. Add practice
2. See summary
3. Read past notes
4. Search notes
5. Weekly goal
6. Edit an entry
7. Exit
Choose an option:
```

Choose **1** to add a session. The program creates `practice.csv` when you save your first entry. That personal file is ignored by Git.

## Try the example

To start with the made-up entries, copy `examples/practice.csv` into the main folder as `practice.csv`. Do this before adding your own entries so you don't replace them.

Choose **2** in the program. You will see:

```text
Practice sessions: 5
On my own: 2
With help: 2
Not yet: 1

Tasks to practise again:
- Turn notes into a study quiz (with help)
```

The article summary no longer appears in the practice list because its latest entry says “on my own.” The summary counts every session; the practice list uses only the latest entry for each task. Task names ignore capital letters and spaces at the ends.

## The next step

I added a few things I would actually use while learning:

**Search notes:** choose 4 and type a word from a task or note. Capital letters don't matter. An empty search shows all entries.

**Weekly goal:** choose 5 to see this week's count or set a new goal. The default is three sessions. A week starts on Monday, and future-dated entries don't count. Every logged session counts, including one where I needed help. The goal repeats each week and saves in `goal.json`, which Git ignores.

**Edit an entry:** choose 6 and pick the entry number shown. Press Enter to keep a field, or type `-` to clear a note. The original date stays the same. The program writes the updated CSV to a temporary file first, then replaces the old file after writing succeeds.

The existing CSV format still works. There is no need to change the example file.

## Python I am practising

Functions, loops, lists, dictionaries, reading and writing CSV files, dates, and handling input errors. I used `Counter` to count results and `pathlib` to work with file paths. The new features add searching strings, comparing dates, saving a small JSON setting, and updating a file safely.

The program does not call an AI model or judge its answers. It records my own experience with a task.

## Check it

```bash
python3 -m unittest discover -s tests -v
```

## What I want to add later

A way to filter notes by date and show how a single task changed over time. I still want to keep the program small enough to understand each part.
