# JARVIS — configurable desktop voice assistant

A local-first desktop assistant prototype with **Python microphone and command handling**, **double-clap activation**, and a **React/Vite animated orb** connected over a local WebSocket.

JARVIS is intended to be **clonable**: each person can configure their own name, microphone, language, project directory and optional voice provider. The current command recognition and responses are primarily **French**; changing the recognition locale does **not** translate or generalize the command parser.

## Supported environment

The current implementation is primarily developed for **Windows**. Some actions rely on Windows APIs or locally installed Chrome/Cursor. Other platforms are not yet verified. You need Python, Node.js/npm, a microphone, and Git for Git-related commands.

## First-time setup

```bash
git clone https://github.com/emma-dasilva-dev/emma-jarvis.git
cd emma-jarvis
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows cmd: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Then install dependencies:

```bash
python -m pip install -r requirements.txt
cd ui
npm ci
cd ..
```

Copy `.env.example` to `.env` (PowerShell: `Copy-Item .env.example .env`; macOS/Linux: `cp .env.example .env`) and edit it for **your own** machine. Do not commit `.env`.

Start the Python assistant and UI together:

```bash
python start_jarvis.py
```

This opens the Vite interface at `http://127.0.0.1:5173`; the state-only WebSocket listens on `127.0.0.1:8765`. Stop with Ctrl+C. You can also run only the Python assistant with `python jarvis.py`.

## User configuration

| Setting | Meaning |
| --- | --- |
| `JARVIS_USER_NAME` | Optional name used in the greeting. Blank gives a generic greeting. |
| `JARVIS_COMMAND_LANGUAGE` | Speech recognition locale; defaults to `fr-FR`. Existing command matching remains French. |
| `JARVIS_INPUT_DEVICE` | Optional microphone index or a substring of its device name. |
| `JARVIS_PROJECT_PATH` | Optional local folder for project and pre-push checks. |
| `JARVIS_GREETING_AUDIO` | Optional WAV from ElevenLabs, relative to the repository or an absolute path. Defaults to `assets/jarvis-welcome.wav` when present. |
| `ELEVENLABS_API_KEY` | Optional ElevenLabs credential for synthesized voice. |
| `ELEVENLABS_VOICE_ID` | Optional voice ID; required alongside the key for speech. |
| `JARVIS_USE_LEGACY_GREETING_AUDIO` | Defaults to false. Explicit opt-in to the original prerecorded audio; it may name the original developer. |

To use a generic recorded welcome, export a 16-bit PCM WAV from ElevenLabs, name it `jarvis-welcome.wav`, and place it in `assets/`. This recording takes precedence over synthesized personalized speech; the generic text appears in the UI when the file is present. Without a recording, spoken personalized greetings require an ElevenLabs key and voice ID. Without credentials, JARVIS can display its greeting but cannot synthesize it. Some other prerecorded command acknowledgements are still bundled and will be generalized in later work.

## Current functionality and limitations

- Detect double claps using the Python microphone stream.
- Capture and recognize short commands; the current command set targets French.
- Open Chrome and run a local project/pre-push check.
- Render idle, listening, processing and speaking states using React and WebSockets.
- ElevenLabs is optional, but not all voice interactions yet have a credential-free fallback.
- This is **not yet** a general-purpose LLM assistant, safe command executor, or fully tested cross-platform application.
- Do not expose the development server or WebSocket port publicly. Review any local commands before running this software.

## Repository hygiene

The original history includes Python bytecode caches and demo audio files. Ignore rules now prevent newly generated caches from being added accidentally, but **previously tracked files remain tracked** until explicitly removed. Existing recordings may be licensed or personal; review redistribution rights before publishing a release. The repository does not yet contain an explicit open-source license; a suitable license must be selected before advertising reuse rights.

## Next milestones

1. Generalize all remaining prerecorded phrases and app-specific actions.
2. Add a safe action registry, with permission checks for potentially destructive commands.
3. Separate configuration, audio detection, transcription, actions and state transport into testable modules.
4. Add automated unit tests and platform verification.
5. Select an open-source license and create a release-ready onboarding experience.
