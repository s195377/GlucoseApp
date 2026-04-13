"""figma_screens.py

HTML screen definitions based on Figma mockups.

How to add a new screen
────────────────────────
1. Design the screen in Figma.
2. Either:
   a) Write the HTML as a file (e.g. my_screen.html) and store its filename, or
   b) Write the HTML inline as a string.
3. Add it to FIGMA_SCREENS under a descriptive key.
4. It will automatically appear in the experiment launcher.
"""


# ── Landing Page ──────────────────────────────────────────────────────────────
# Figma: Project-Overview → node 56-373
# Source: index.html

LANDING_HTML = "index.html"


# ── Screen registry ───────────────────────────────────────────────────────────
# Values can be a filename (e.g. "index.html") or an inline HTML string.

FIGMA_SCREENS: dict[str, str] = {
    "Landing Page": LANDING_HTML,
}
