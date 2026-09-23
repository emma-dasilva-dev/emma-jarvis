#!/usr/bin/env python3
"""Start the Jarvis UI and Python assistant together."""

from __future__ import annotations

import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

import jarvis

ROOT = Path(__file__).resolve().parent
UI_DIR = ROOT / "ui"
UI_URL = "http://127.0.0.1:5173"
UI_HOST = "127.0.0.1"
UI_PORT = 5173


def _wait_for_ui_and_open() -> None:
    deadline = time.monotonic() + 20.0
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((UI_HOST, UI_PORT), timeout=0.5):
                webbrowser.open(UI_URL)
                return
        except OSError:
            time.sleep(0.25)


def _start_ui() -> subprocess.Popen:
    npm = "npm.cmd" if sys.platform == "win32" else "npm"

    if not (UI_DIR / "node_modules").exists():
        raise RuntimeError(
            "UI dependencies are missing. Run 'cd ui' then 'npm install' once."
        )

    flags = 0
    if sys.platform == "win32":
        flags = subprocess.CREATE_NO_WINDOW

    return subprocess.Popen(
        [npm, "run", "dev", "--", "--host", UI_HOST],
        cwd=UI_DIR,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=flags,
    )


def main() -> int:
    print("Starting Jarvis...")
    ui_process = _start_ui()

    threading.Thread(
        target=_wait_for_ui_and_open,
        daemon=True,
        name="jarvis-ui-opener",
    ).start()

    try:
        return jarvis.main()
    finally:
        if ui_process.poll() is None:
            ui_process.terminate()
            try:
                ui_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ui_process.kill()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Jarvis startup error: {exc}")
        raise SystemExit(1)
