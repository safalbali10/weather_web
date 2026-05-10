# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Claude Code Instructions for Safal

## About Me
- My name is Safal
- I am learning Claude Code from scratch and I am a beginner

## Code Style Preferences
- Keep all code simple, clean and well commented
- Always explain what each function does
- Never use complex code without explaining it clearly
- I prefer Python 3

## Running Scripts

Run any Python script from the terminal:
```bash
python3 ~/projects/calculator.py
python3 ~/projects/todo.py
python3 ~/projects/password_generator.py
python3 "~/my first project/hello.py"
```

No build step or dependency installation needed — all scripts use Python's standard library only.

## Project Structure

- `~/projects/calculator.py` — interactive CLI calculator (add, subtract, multiply, divide). Runs as a loop until the user quits.
- `~/projects/todo.py` — CLI to-do list app. Tasks are persisted to `~/projects/todo_tasks.json` as a JSON array of `{name, done}` objects. Loads on start, saves after every change.
- `~/projects/password_generator.py` — CLI password generator. Lets the user pick length and character types, shows 5 options, and appends the chosen password to `~/projects/saved_passwords.txt`.
- `~/my first project/hello.py` — first Python script, prints a greeting.
- `~/my first project/hello.txt` — personal learning note.
