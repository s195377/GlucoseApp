"""_html_runner.py

Internal utility: local HTTP server + pywebview launcher.
Shared by landing_environment and experiment_environment.
"""

import functools
import http.server
import os
import shutil
import socket
import socketserver
import tempfile
import threading
import time
import webview

# Root of the project (one level above the app/ package)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _find_free_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _start_html_server(html: str) -> int:
    tmpdir = tempfile.mkdtemp()
    with open(os.path.join(tmpdir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    # copy data/ directory so the page can fetch local CSV files
    data_src = os.path.join(BASE_DIR, "data")
    if os.path.isdir(data_src):
        shutil.copytree(data_src, os.path.join(tmpdir, "data"))
    port = _find_free_port()
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=tmpdir
    )
    Handler.log_message = lambda *_: None
    server = socketserver.TCPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return port


def run(title: str, html: str) -> None:
    """Serve *html* over localhost and open it in a webview window."""
    port = _start_html_server(html)
    time.sleep(0.2)
    webview.create_window(
        title,
        url=f"http://127.0.0.1:{port}/index.html",
        width=1280, height=860, resizable=True,
    )
    webview.start()
