# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SSSIHMS-AVAS (Automated Voice Announcement System) is a Python 2.7 Flask application used at SSSIHMS hospital (Sri Sathya Sai Institute of Higher Medical Sciences) to make automated blood requirement announcements over speakers. It plays background bhajan music (via Radio Sai stream or local playlists) and pauses music to make announcements when blood is needed.

## Running the Application

```bash
python AVAS.py
```

The Flask server starts on `0.0.0.0:5000`. No build step or test suite exists.

## Dependencies

Required packages: `flask`, `pyaudio`, `pygame`, `schedule`, `python-vlc`, `pycaw`, `comtypes`, `easygui`, `wave`. The `pycaw`/`comtypes` packages are Windows-only (volume control). See `packages to be installed/` directory for details.

## Architecture

### Core Modules

- **AVAS.py** — Main entry point. Flask web server with routes for login, blood requests, user management, and admin. Spawns two threads: the Flask server and the bhajan player. Uses Windows audio APIs (`pycaw`) to control system volume during announcements.
- **Audio.py** — Audio playback engine. Plays `.wav` announcement files via `pyaudio`, manages bhajan playback via `pygame.mixer` or VLC stream (`stream.radiosai.org:8000`). Contains `pause()`/`unpause()` to interrupt music for announcements.
- **Utils.py** — GUI-based login dialog (`easygui`) and user validation against `user/user_details.txt`. Also contains an admin control panel.
- **globals.py** — Shared global state variables (`flag`, `str_var`, `stream_or_game`, `vlc_player`).

### Audio Flow

1. Background bhajans play continuously (either VLC stream or local playlist from `playlist/<DayOfWeek>/`)
2. Blood request received → music pauses → system volume raised → announcement WAV files play → "I repeat" → announcement replays → volume lowered → music resumes

### Key Directories

- **audio/** — Numbered `.wav` files for announcement segments (intro, blood group names, closing). Subdirs: `bloodgroup/` (per-group audio), `only_groups/` (group-name-only audio)
- **templates/** — Flask HTML templates (login, home, admin, error pages). CSS is in `templates/style.css`
- **static/** — Images served to the browser
- **playlist/** — Daily bhajan playlists organized by day-of-week subdirectories
- **user/** — `user_details.txt` stores credentials in `USERNAME:PASSWORD` format
- **AVAS Versions/** — Historical versions of the main script

### User Authentication

Plain-text file-based auth via `user/user_details.txt`. Users can be added through the web UI or by editing the file directly (format: `USERNAME:PASSWORD`, one per line).

## Important Notes

- The codebase is Python 2.7 (uses `print` statements without parentheses in some files, `urllib.urlopen`)
- Windows-specific: Volume control via `pycaw`/`comtypes` will not work on macOS/Linux
- The `stream_or_game` global determines audio source: `0` = VLC stream, `1` = pygame local playlist
- There are known bugs in the code (e.g., undefined variable `i` used instead of `count` in Audio.py, typo `scheduke` in `bhajans_stop`)
