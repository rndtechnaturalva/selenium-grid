# Selenium Grid via Docker Compose

Selenium Grid 4 with Chrome, Firefox, and Edge nodes, VNC access, and video recording baked in for local or CI usage.

## Requirements

- Docker Desktop 4.0+ with Compose V2 (`docker compose` command)
- At least 6 GB of free RAM (each browser node starts with 2 GB shared memory)

## What's inside

| Service | Image | Purpose | Ports |
| --- | --- | --- | --- |
| `selenium-hub` | `selenium/hub:${SELENIUM_VERSION}` | Routes and manages sessions | 4442-4444 |
| `selenium-node-chrome` | `selenium/node-chrome:${SELENIUM_VERSION}` | Chrome browser with VNC & recording | 5900 (VNC), 7900 (noVNC) |
| `selenium-node-firefox` | `selenium/node-firefox:${SELENIUM_VERSION}` | Firefox browser with VNC & recording | 5901, 7901 |
| `selenium-node-edge` | `selenium/node-edge:${SELENIUM_VERSION}` | Edge browser with VNC & recording | 5902, 7902 |
| `selenium-video-processor` | `selenium/video:${SELENIUM_VIDEO_TAG}` | Processes session recordings | — |

Session videos are saved to `./videos`, while Grid logs land in `./logs`.

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

### Video output

Each completed session writes `*.mp4` files into the `videos` folder. Clean it periodically to avoid filling up disk space.

## Configuration reference

All key settings live in `.env`:

- `SELENIUM_VERSION` and `SELENIUM_VIDEO_TAG` keep the stack on a matching release.
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

- Persist the `videos/` and `logs/` directories as artifacts for debugging.
- Use `docker compose pull` during CI warmup to avoid cold-start delays.
- Increase `SE_SESSION_TIMEOUT` for long suites or reduce it if you want faster cleanup of orphan sessions.

## Troubleshooting

- **Browser sessions never start**: ensure ports 4442-4444 are free and Docker Desktop has enough memory.
- **Video files are empty**: confirm the `selenium-video-processor` container is running and the `videos/` directory is writable.
- **VNC refuses connection**: some clients require the `vnc://` scheme (e.g., `vnc://localhost:5900`).
