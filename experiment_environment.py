"""experiment_environment.py

Experiment environment for testing HTML scripts.

Uses pywebview + a local HTTP server to render HTML with full browser engine
(WKWebView on macOS).  Serving over http://127.0.0.1 gives the page a real
origin so ES module imports from external CDNs work — including ObservableHQ:

  import { Runtime, Inspector }
    from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@5/dist/runtime.js";
  import define
    from "https://api.observablehq.com/d/<id>.js?v=3";

How to add a new script
───────────────────────
1. Write the HTML string (or point to a local .html file path) below.
2. Add it to HTML_SCRIPTS under a descriptive key.
3. Pass that key to run(), or pick it from the launcher in main.py.
"""

import functools
import http.server
import os
import socketserver
import tempfile
import threading
import time
import webview
import figma_screens

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ── HTML scripts ──────────────────────────────────────────────────────────────
# Figma-based screens live in figma_screens.py.
# LANDING_HTML is imported from there so the styled version is always the default.

LANDING_HTML = figma_screens.LANDING_HTML


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
    src="https://observablehq.com/embed/@dtu/blood-glucose-project@332?cell=*&api_key=fa58c6bfbf2d68b6afb83b92bc47b985ec8bc55d"
    frameborder="0"
    allowfullscreen>
  </iframe>
</body>
</html>"""



# ── Scripts registry ──────────────────────────────────────────────────────────

HTML_SCRIPTS: dict[str, str] = {
    **figma_screens.FIGMA_SCREENS,          # all Figma-designed screens
    "ObservableHQ Embed": OBSERVABLE_EMBED_HTML,
}


# ── Local HTTP server ─────────────────────────────────────────────────────────

def _find_free_port() -> int:
    """Return an available TCP port on localhost."""
    import socket
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _start_html_server(html: str) -> int:
    """
    Write *html* to a temp directory, start a background HTTP server,
    and return the port it is listening on.

    Serving over http://127.0.0.1 gives the page a real origin so that
    ES module imports from external CDNs are not blocked by CORS/null-origin.
    """
    tmpdir = tempfile.mkdtemp()
    with open(os.path.join(tmpdir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)

    port = _find_free_port()
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=tmpdir,
    )
    Handler.log_message = lambda *_: None  # silence per-request console output

    server = socketserver.TCPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return port


# ── Runner ────────────────────────────────────────────────────────────────────

def load_script(name: str) -> str:
    """Return HTML content for *name*.

    Values in HTML_SCRIPTS can be either:
    - A raw HTML string (returned as-is), or
    - A filename like "index.html" (resolved relative to BASE_DIR).
    """
    content = HTML_SCRIPTS.get(name, LANDING_HTML)
    if content.endswith(".html"):
        path = content if os.path.isabs(content) else os.path.join(BASE_DIR, content)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                return fh.read()
    return content


def run(script_name: str = "Landing Page") -> None:
    """Serve the chosen HTML script over localhost and open it in a webview window."""
    html = load_script(script_name)
    port = _start_html_server(html)
    time.sleep(0.2)  # give the server a moment to bind

    webview.create_window(
        f"Experiment — {script_name}",
        url=f"http://127.0.0.1:{port}/index.html",
        width=1280,
        height=860,
        resizable=True,
    )
    webview.start()


# ── Stand-alone launcher ──────────────────────────────────────────────────────

if __name__ == "__main__":
    run("ObservableHQ Embed")
