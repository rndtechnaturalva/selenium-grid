# Selenium Grid via Docker Compose

Selenium Grid 4 with Chrome, Firefox, and Edge nodes plus VNC access for local or CI usage.

## Requirements

- Docker Desktop 4.0+ with Compose V2 (`docker compose` command)
- At least 6 GB of free RAM (each browser node starts with 2 GB shared memory)

## What's inside

| Service | Image | Purpose | Ports |
| --- | --- | --- | --- |
| `selenium-hub` | `selenium/hub:${SELENIUM_VERSION}` | Routes and manages sessions | 4442-4444 |
| `selenium-node-chrome` | `selenium/node-chrome:${SELENIUM_VERSION}` | Chrome browser with VNC | 5900 (VNC), 7900 (noVNC) |
| `selenium-node-firefox` | `selenium/node-firefox:${SELENIUM_VERSION}` | Firefox browser with VNC | 5901, 7901 |
| `selenium-node-edge` | `selenium/node-edge:${SELENIUM_VERSION}` | Edge browser with VNC | 5902, 7902 |

Grid logs land in `./logs` for easy inspection, and each node now advertises the public URI `http://${PUBLIC_GRID_HOST}:${PUBLIC_NODE_PORT}` in the Grid UI.

## Getting started

1. Tweak `.env` if you need different versions or screen dimensions.
2. Launch the grid:

```powershell
docker compose up -d
```

3. Visit the Grid console at <http://localhost:4444/ui> to watch sessions connect.

### Useful commands

- Tail hub logs

  ```powershell
  docker compose logs -f selenium-hub
  ```

- Stop and clean everything

  ```powershell
  docker compose down -v
  ```

### VNC and noVNC access

- Chrome: `vnc://localhost:5900` or <http://localhost:7900>
- Firefox: `vnc://localhost:5901` or <http://localhost:7901>
- Edge: `vnc://localhost:5902` or <http://localhost:7902>

No passwords are required (`SE_VNC_NO_PASSWORD=1`).

### Optional video recording

The stack ships without the ffmpeg video sidecar to keep things light for pure automation. If you need session recordings:

1. Restore the `selenium/video` service and related environment variables from the `video-processor` block in `docker-compose.yml`.
2. Reintroduce the `SELENIUM_VIDEO_TAG` and `VIDEO_OUTPUT` entries in `.env` (for example `SELENIUM_VIDEO_TAG=ffmpeg-4.22.0-20241004`).
3. Re-add `SE_VIDEO_RECORD_SESSION=true` and `SE_VIDEO_PATH=/opt/selenium/videos` to each node service and mount the video volume.

Once those pieces are back, recordings will be emitted to the `videos/` directory.

## Configuration reference

All key settings live in `.env`:

- `SELENIUM_VERSION` keeps hub and nodes aligned to the same release.
- `PUBLIC_GRID_HOST` and `PUBLIC_NODE_PORT` control the URI shown in the Grid UI (and in node metadata). Set this to a hostname users can reach, such as `selenium.nhi.co.id`.
- `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `SCREEN_DEPTH` control the virtual display.
- `SE_SESSION_TIMEOUT` and `SE_SESSION_REQUEST_TIMEOUT` help tune long-running workflows.
- `SE_NODE_MAX_SESSIONS` plus `SE_NODE_OVERRIDE_MAX_SESSIONS` let you scale concurrency per node.

## Health check from code

A minimal Python test script (`tests/ping_grid.py`) is included. It spins up a Chrome session through the Grid, fetches example.com, and quits. Run it after the containers are healthy to confirm end-to-end functionality.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tests\ping_grid.py
```

> Tip: Run `docker compose ps` to ensure the Chrome node is `Running` before executing the script.

## CI pointers

- Persist the `logs/` directory as build artifacts for debugging.
- Use `docker compose pull` during CI warmup to avoid cold-start delays.
- Increase `SE_SESSION_TIMEOUT` for long suites or reduce it if you want faster cleanup of orphan sessions.

## Troubleshooting

- **Browser sessions never start**: ensure ports 4442-4444 are free and Docker Desktop has enough memory.
- **VNC refuses connection**: some clients require the `vnc://` scheme (e.g., `vnc://localhost:5900`).
