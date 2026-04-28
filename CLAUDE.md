# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A Python research tool for conducting structured user experiments on glucose-tracking visualizations. Participants interact with 7 different chart types, click answers to tasks, and provide feedback. Results are stored in CSV files for analysis.

## Setup

```bash
# Conda (preferred)
conda env create -f environment.yml
conda activate glukoseTrackingProject

# Or pip
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python3 main.py                        # Tkinter launcher (3-button menu)
python3 app/experiment_environment.py  # Experiment session directly
python3 app/test_environment.py        # Likert/feedback test session directly
python3 app/landing_environment.py     # Landing page prototype directly
```

There are no automated tests.

## Architecture

**Three independent environments**, each launched from `main.py` via Tkinter buttons:

### Shared infrastructure (`app/_html_runner.py`)
Copies `data/` into a temp directory, starts a local HTTP server on a random free port, and opens a `pywebview` window. All HTML-based environments use this.

### Experiment Environment (`app/experiment_environment.py`, ~1900 lines)
The core tool. Flow:
1. Researcher enters participant ID → Latin-square slot assigned via `full_order_for_slot()` in `experiment_config.py`
2. `pywebview` loads an HTML visualization with injected JS that records clicks
3. On window close, JS POSTs click data back to Python
4. Python scores each task via `evaluate_answer()` using criteria defined in `experiment_config.py`
5. Researcher confirms scores and enters notes
6. Results written to `experiment_sessions.csv` via `session_logger.py`

### Test Environment (`app/test_environment.py`)
Pure Tkinter multi-screen flow: instructions → think-aloud text → Likert scales → comparative preference → writes `sessions.csv`.

### Landing Environment (`app/landing_environment.py`)
Loads `index.html` (the main phone-frame prototype UI, ~62KB) via `_html_runner.py`.

## Key configuration (`app/experiment_config.py`)

- **7 conditions**: `daily_line`, `daily_bar`, `weekly_bar`, `weekly_line`, `monthly`, `monthly_line`, `monthly_bar`
- **21 tasks** (3 per condition), each with a `criteria_type` that `evaluate_answer()` uses for auto-scoring
- **Latin-square counterbalancing**: `full_order_for_slot(slot)` returns the 7-condition sequence for a given participant slot
- Day/Week order alternates by slot (even/odd); Month order cycles through 6 permutations

## Data

- `data/bg_data_combined.csv` — glucose readings (July–Sept 2024), served statically to HTML pages
- `experiment_sessions.csv` — one row per experiment session; columns include per-condition task scores and open-ended feedback
- `sessions.csv` — one row per test session (Likert responses, comparative choice)

## macOS dependency

`pyobjc-core`, `pyobjc-framework-cocoa`, and `pyobjc-framework-webkit` are required for `pywebview` on macOS. This project is macOS-only as currently configured.