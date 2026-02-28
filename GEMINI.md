# yewtube (yt) - Terminal YouTube Player

This directory is a specialized workspace for **yewtube** (a fork of `mps-youtube`), a terminal-based YouTube player and downloader that does not require a YouTube API key.

## Project Overview

- **Purpose**: Search, stream, and download YouTube content directly from the command line.
- **Core Technologies**: Python 3.x, `yt-dlp`, `requests`, `pafy`, and `youtube-search-python`.
- **Playback Engines**: Supports `mpv`, `mplayer`, and `VLC`.
- **Architecture**: A terminal-based interactive CLI that interfaces with YouTube's web interface (via `pafy` and `yt-dlp`) to bypass API requirements.

## Environment & Tools

The project is managed via a `uv` virtual environment located in `.venv/`.

### Key Executables
- `yt`: The main interactive terminal interface.
- `yt-dlp`: The underlying engine used for downloading and extracting media information.

## Usage Guide

To start the interface, run:
```bash
./.venv/bin/yt
```

### Common Commands (Internal to `yt`)
- `/ <search terms>`: Search for videos.
- `// <search terms>`: Search for playlists.
- `1-5`: Play videos 1 through 5.
- `d 1`: Download video 1.
- `set <option> <value>`: Configure settings (e.g., `set player mpv`).
- `h`: Show help.

## Development Context

- **Fork Status**: This is a fork of the original `mps-youtube` project, maintained to ensure continued functionality without official API keys.
- **Configuration**: User configuration and local playlists are typically stored in `~/.config/mps-youtube` or `~/.config/yewtube`.
- **Dependencies**: Relies heavily on `yt-dlp` for extracting streams. If playback fails, updating `yt-dlp` is often the first step:
  ```bash
  ./.venv/bin/python -m pip install -U yt-dlp
  ```

## Troubleshooting

If you encounter `ModuleNotFoundError: No module named 'pip'` when running `yt`, it may be due to the specific `uv` environment configuration. Ensure all dependencies are correctly linked in `site-packages`.
