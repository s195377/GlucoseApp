# glukoseTrackingProject

A Python research tool for testing and evaluating glucose-tracking visualisations.
It consists of two independent environments — an **experiment environment** for displaying
interactive visualisations, and a **test environment** for collecting structured participant responses.

---

## Setup & Requirements

Choose one of the following methods to ensure you have the correct dependencies (pywebview, pyobjc, etc.).

### Option A: Conda
```bash
conda env create -f environment.yml
conda activate glukoseTrackingProject

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

---

## Project structure

| Path | Description |
|---|---|
| `main.py` | Launcher — opens a picker to choose what to run |
| `app/experiment_environment.py` | Serves HTML visualisation screens in a webview window |
| `app/test_environment.py` | Multi-screen test session (instructions → writing → Likert → comparative) |
| `app/figma_screens.py` | Registry of all Figma-based HTML screens |
|  data/bg_data_combined.csv  | Source dataset for visualisations
| `index.html` | Phone-frame prototype UI (Landing Page screen) |

---

## Experiment Environment

`app/experiment_environment.py`renders HTML screens inside a native webview window
 using pywebview. It spins up a local HTTP server so that pages with ES module imports work 
 correctly.

### Two ways to launch

**1. Via the shared launcher (recommended)**

```bash
python3 main.py
```

**2. Directly (opens ObservableHQ Embed immediately)**

```bash
python3 app/experiment_environment.py
```

## Test Environment

`app/test_environment.py` runs a guided four-screen session for collecting participant feedback:

1. **Info screen** — displays onboarding instructions and a *Start* button.
2. **Writing screen** — free-text think-aloud prompt.
3. **Likert screen** — two sets of four 5-point scale questions (Short-term and Long-term feedback).
4. **Comparative screen** — preference choice between feedback types with an open explanation field.

Each completed session is saved as a row in `data/sessions.csv` with a unique test ID.

### Launch

```bash
python3 app/test_environment.py
```

Or via the shared launcher:

```bash
python3 main.py
```

---

## index.html — Landing Page

`index.html` is a self-contained HTML prototype that simulates a mobile phone UI. It is 
registered as the Landing Page entry in `app/figma_screens.py` and loads as the default 
screen in the experiment environment.


### Figma origin

The graphic layout of `index.html` was created from a **Figma mockup**
(Project-Overview, node 56-373). It is registered as the *Landing Page* entry in
`app/figma_screens.py` and loads automatically as the default screen in the experiment environment.

---

## Running the full application

```bash
python3 main.py
```

From the launcher, choose either **Open Visualisation** to view a screen in the experiment
environment, or **Run Test Session** to start a participant test session.
