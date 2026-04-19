"""experiment_environment.py

Experiment environment — ObservableHQ embed and any future experiment screens.
Entry point: run()
"""

try:
    from . import _html_runner
except ImportError:
    import _html_runner         # run directly: python app/experiment_environment.py


OBSERVABLE_EMBED_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>ObservableHQ — Blood Glucose Project</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #fff; }
    iframe { display: block; width: 100%; height: 100vh; border: none; }
  </style>
</head>
<body>
  <iframe
    src="https://observablehq.com/embed/@dtu/blood-glucose-project@419?cell=*&api_key=fa58c6bfbf2d68b6afb83b92bc47b985ec8bc55d"
    frameborder="0"
    allowfullscreen>
  </iframe>
</body>
</html>"""


HTML_SCRIPTS: dict[str, str] = {
    "ObservableHQ Embed": OBSERVABLE_EMBED_HTML,
}


def run(script_name: str = "ObservableHQ Embed") -> None:
    """Open the chosen experiment script in a webview window."""
    html = HTML_SCRIPTS.get(script_name, OBSERVABLE_EMBED_HTML)
    _html_runner.run(f"Glucosee — {script_name}", html)


if __name__ == "__main__":
    run()
