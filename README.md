# Hand Gesture Mouse & Media Controller

A Python project that lets you control your mouse, scrolling, volume, and media playback using hand gestures with a webcam.

## Features

- Move mouse cursor with right-hand index finger
- Left hand:
  - Thumb + index pinch (quick) → Left click
  - Thumb + index pinch (hold) → Drag & drop
  - Thumb + middle pinch → Right click
  - Move up/down → Scroll
  - Move left/right (in upper area) → Volume control
  - Thumb + ring pinch (middle area) → Next track
  - Thumb + pinky pinch (middle area) → Play / Pause
- Two-hand pinch (middle area) → Zoom in / out (`Ctrl + +` / `Ctrl + -`)
- `E` key → Toggle "Air Mode" on/off
- `Q` key → Quit app

## Requirements

- Python 3.10
- Webcam
- Packages from `requirements.txt`:

```bash
pip install -r requirements.txt
