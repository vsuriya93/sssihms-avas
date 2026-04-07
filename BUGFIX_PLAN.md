# AVAS Bug Fix Plan

## Phase 1: Critical — App Cannot Start

These bugs prevent the application from launching at all.

### 1.1 IndentationError in AVAS.py (line 42)
- **File:** `AVAS.py:42`
- **Bug:** `stream_or_game=1` is indented inside no block
- **Fix:** Remove the leading tab so it aligns with surrounding module-level code

### 1.2 Missing `import vlc` in globals.py (line 16)
- **File:** `globals.py:16`
- **Bug:** `vlc.MediaPlayer(url)` called without importing `vlc`
- **Fix:** Add `import vlc` at the top of globals.py

### 1.3 Missing `authenticate_user()` function (AVAS.py lines 94, 129)
- **File:** `AVAS.py`
- **Bug:** `authenticate_user(result)` is called in `bloodRequest()` and `admin_home()` but never defined or imported
- **Fix:** Define `authenticate_user()` in AVAS.py that reads `user/user_details.txt`, compares credentials from `result` form data, and sets `session['logged_in']`. Reference the older version in `AVAS Versions/avas.py` for the original implementation

### 1.4 `bhajans_play` called without required argument (AVAS.py line 192)
- **File:** `AVAS.py:192`
- **Bug:** `run_thread(bhajans_play)` but `bhajans_play(vlc_val)` expects an argument
- **Fix:** Either pass a default argument via `threading.Thread(target=bhajans_play, args=(0,))` or make `vlc_val` optional with a default value in Audio.py

---

## Phase 2: Runtime Crashes — Errors Hit During Normal Use

These bugs crash the app when specific features are used.

### 2.1 Undefined variable `i` used instead of `count` (Audio.py lines 55, 65, 75)
- **File:** `Audio.py`
- **Bug:** `play_blood_names()`, `play_blood_groups()`, and `play_group()` all reference `i` instead of `count`
- **Fix:** Replace `i` with `count` in all three functions

### 2.2 Missing quotes on `passwd-rep` (AVAS.py line 147)
- **File:** `AVAS.py:147`
- **Bug:** `result[passwd-rep]` — `passwd` and `rep` are undefined variables
- **Fix:** Change to `result['passwd-rep']`

### 2.3 `session['logged_in']` KeyError on first login (AVAS.py line 97)
- **File:** `AVAS.py:97`
- **Bug:** `session['logged_in']` accessed before being set
- **Fix:** Use `session.get('logged_in')` or initialize it inside `authenticate_user()`

### 2.4 `day()` function not defined (Audio.py line 130)
- **File:** `Audio.py:130`
- **Bug:** `bhajans_play()` calls `playlist, cur_day = day()` but no such function exists
- **Fix:** Import or define a `day()` function that returns `(playlist_files, day_name)`. Likely should use `Utils.get_day()` after fixing it to return values, plus `os.listdir()` to get the playlist

### 2.5 Missing easygui import in Utils.py (lines 35, 73)
- **File:** `Utils.py`
- **Bug:** `multpasswordbox` and `buttonbox` used without importing `easygui`
- **Fix:** Add `from easygui import *` at the top of Utils.py

### 2.6 `valid()` vs `validate()` name mismatch (Utils.py line 68)
- **File:** `Utils.py:68`
- **Bug:** Calls `valid(fieldValues)` but function is named `validate()`
- **Fix:** Change `valid(fieldValues)` to `validate(fieldValues)`

### 2.7 Undefined variable `p` in Admin_box() (Utils.py lines 75-79)
- **File:** `Utils.py:75-79`
- **Bug:** `p.pause()`, `p.play()`, `p.stop()` — `p` is never defined
- **Fix:** Replace with direct `pygame.mixer.music` calls or import the `pause`/`unpause` functions from Audio.py

---

## Phase 3: Logic Errors — Wrong Behavior

These don't crash but produce incorrect results.

### 3.1 `play_audio()` uses stream after closing (Audio.py lines 30-35)
- **File:** `Audio.py:30-35`
- **Bug:** When stop is triggered (`str_var==0 and flag==1`), stream is closed and PyAudio terminated, but the loop continues and tries to write to the closed stream
- **Fix:** Add `return` after terminating, so the function exits cleanly after cleanup

### 3.2 `pause()`/`unpause()` unconditionally call VLC (Audio.py lines 149-161)
- **File:** `Audio.py:149-161`
- **Bug:** Both functions call `vlc_player.stop()`/`vlc_player.play()` before checking `stream_or_game`, so VLC is always invoked even in pygame mode
- **Fix:** Remove the unconditional VLC calls; only call VLC inside the `stream_or_game==0` branch

### 3.3 Typo `scheduke.CancelJob` (Audio.py line 147)
- **File:** `Audio.py:147`
- **Bug:** Misspelled `schedule` as `scheduke`. Also unreachable after `sys.exit()`
- **Fix:** Fix spelling to `schedule` and move it before `sys.exit()`, or remove the unreachable line

### 3.4 `get_day()` returns nothing (Utils.py lines 8-26)
- **File:** `Utils.py:8-26`
- **Bug:** Sets local `day` but never returns it
- **Fix:** Add `return day` at the end. Also simplify — the chain of if-statements all do the same thing; `day = now.strftime("%A")` is sufficient

### 3.5 String identity comparison with `is` (Utils.py lines 74-80)
- **File:** `Utils.py:74-80`
- **Bug:** `reply is "pause"` uses identity (`is`) instead of equality (`==`)
- **Fix:** Change all `is` comparisons to `==`

### 3.6 `exit()` shadows built-in (Audio.py line 163)
- **File:** `Audio.py:163`
- **Bug:** `def exit()` shadows Python's built-in
- **Fix:** Rename to `exit_app()` or `avas_exit()`

---

## Execution Order

1. Fix Phase 1 (all 4 items) — app can start
2. Fix Phase 2 (all 7 items) — core features work without crashing
3. Fix Phase 3 (all 6 items) — correct behavior

Total: 17 bugs across 4 files.
