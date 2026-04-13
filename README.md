# glukoseTrackingProject

A Python research tool for testing and evaluating glucose-tracking visualisations.
It consists of two independent environments — an **experiment environment** for displaying
interactive visualisations, and a **test environment** for collecting structured participant responses.

---

## Requirements

Install dependencies before running:

```bash
pip install pywebview
```

---

## Project structure

| File | Description |
|---|---|
| `main.py` | Launcher — opens a picker to choose what to run |
| `experiment_environment.py` | Serves HTML visualisation screens in a webview window |
| `test_environment.py` | Multi-screen test session (instructions → writing → Likert → comparative) |
| `figma_screens.py` | Registry of all Figma-based HTML screens |
| `index.html` | Phone-frame prototype UI (Landing Page screen) |

---

## Experiment Environment

`experiment_environment.py` renders HTML screens inside a native webview window using
[pywebview](https://pywebview.flowrl.com/). It spins up a local HTTP server so that
pages with ES module imports (e.g. ObservableHQ embeds) work correctly across all platforms.

### Two ways to launch

**1. Via the shared launcher (recommended)**

```bash
python3 main.py
```

Opens a picker window where you can select which visualisation screen to display before launching.
All screens registered in `figma_screens.py` and the ObservableHQ embed appear as options.

**2. Directly (opens ObservableHQ Embed immediately)**

```bash
python3 experiment_environment.py
```

Skips the picker and opens the ObservableHQ Embed screen straight away.

### Adding a new screen

1. Design the screen in Figma and export / write it as HTML.
2. Either save it as a `.html` file next to the project, or write it as an inline string.
3. Add it to `FIGMA_SCREENS` in `figma_screens.py` under a descriptive key.
4. It will automatically appear in the launcher picker.

---

## Test Environment

`test_environment.py` runs a guided four-screen session for collecting participant feedback:

1. **Info screen** — displays onboarding instructions and a *Start* button.
2. **Writing screen** — free-text think-aloud prompt.
3. **Likert screen** — two sets of four 5-point scale questions (Short-term and Long-term feedback).
4. **Comparative screen** — preference choice between feedback types with an open explanation field.

Each completed session is saved as a row in `sessions.csv` with a unique test ID.

### Launch

```bash
python3 test_environment.py
```

Or via the shared launcher:

```bash
python3 main.py
```

---

## index.html — Landing Page

`index.html` is a self-contained HTML prototype that simulates a mobile phone UI.
It renders a navigable phone-frame with multiple screens:

- **Profile** — user overview with navigation to data and settings.
- **Upload data** — file upload / QR scan options.
- **Settings** — placeholder screen.
- **Blood sugar (Calendar / Daily / Weekly)** — embedded ObservableHQ visualisations.

### Figma origin

The graphic layout of `index.html` was created from a **Figma mockup**
(Project-Overview, node 56-373). It is registered as the *Landing Page* entry in
`figma_screens.py` and loads automatically as the default screen in the experiment environment.

---

## Running the full application

```bash
python3 main.py
```

From the launcher, choose either **Open Visualisation** to view a screen in the experiment
environment, or **Run Test Session** to start a participant test session.
