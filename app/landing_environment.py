"""landing_environment.py

Loads and displays the Figma-based landing page (index.html).
Entry point: run()
"""

import os

try:
    from . import figma_screens
    from . import _html_runner
except ImportError:
    import figma_screens        # run directly: python app/landing_environment.py
    import _html_runner


def _load() -> str:
    """Read index.html from the project root and return its contents."""
    content = figma_screens.LANDING_HTML
    if content.endswith(".html"):
        path = (
            content
            if os.path.isabs(content)
            else os.path.join(_html_runner.BASE_DIR, content)
        )
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                return fh.read()
    return content


def run() -> None:
    """Open the landing page in a webview window."""
    _html_runner.run("Glucosee — Landing Page", _load())


if __name__ == "__main__":
    run()
