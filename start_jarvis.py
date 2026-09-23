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
PRE_PUSH_AUDIO = ROOT / "assets" / "pre-push-check.wav"


def _install_pre_push_command() -> None:
    """Add the short French pre-push command without disturbing stable voice capture."""
    original_handler = jarvis.handle_voice_command

    def handle_voice_command(command: str, stream) -> None:
        normalized = jarvis._normalize_french_command(command)
        is_pre_push = (
            "controle pre-push" in normalized
            or "controle pre push" in normalized
            or "pre-push" in normalized
            or "pre push" in normalized
        )

        if not is_pre_push:
            original_handler(command, stream)
            return

        jarvis.set_jarvis_state("processing", "Contrôle pré-push…")
        project_result = jarvis.check_project()
        result_message = jarvis._project_check_message(project_result)

        jarvis.set_jarvis_state("speaking", result_message)
        stream.stop()
        try:
            jarvis.play_local_audio(PRE_PUSH_AUDIO, "Pre-push check")
        finally:
            stream.start()

    jarvis.handle_voice_command = handle_voice_command


_install_pre_push_command()


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
