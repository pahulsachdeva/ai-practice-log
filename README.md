I tried taking computer science courses, and I tried learning Python at Colgate University. My major was neuroscience, but I ended up trying anyway. I went through Computer Science 101 and 102, but I feel like I can do much better.

I now work for an AI company, and I want to understand more of the technical side. This is my first Python project here. I wanted to start with something small that I could understand, use, and keep improving.

# AI Practice Log

A simple Python program to keep track of tasks I practise with an AI assistant.

Knowing about a feature and being able to use it on my own are two different things. I wanted a small place to record what I tried, how it went, and what I should practise again.

## What it does

- Saves a task, the date, how it went, and an optional note.
- Lets me choose **on my own**, **with help**, or **not yet**.
- Shows how many sessions I logged under each result.
- Lists tasks to practise again, based on the latest entry for each task.
- Keeps past notes in a CSV file I can open and read.

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
4. Exit
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

## Python I am practising

Functions, loops, lists, dictionaries, reading and writing CSV files, dates, and handling input errors. I used `Counter` to count results and `pathlib` to work with file paths.

The program does not call an AI model or judge its answers. It records my own experience with a task.

## Check it

```bash
python3 -m unittest discover -s tests -v
```

## What I want to add later

A way to search past notes and a weekly practice goal. For now, I want to keep the program small and understand each part.
