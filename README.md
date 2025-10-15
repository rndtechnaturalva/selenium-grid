# Browserless Automation Stack

This project packages [browserless](https://www.browserless.io/) via Docker Compose so you can run headless Chrome for automation, scraping, or testing without maintaining a full Selenium Grid.

## Requirements

- Docker Desktop 4.0+ with Compose V2 (`docker compose` command)
- Roughly 2 GB of free RAM per concurrent Chrome session (adjust via `.env`)

## What's inside

| Service | Image | Purpose | Ports |
| --- | --- | --- | --- |
| `browserless` | `browserless/chrome:${BROWSERLESS_TAG}` | Headless Chrome runtime with browserless API & WebDriver bridge | (internal) |
| `nginx` | `nginx:alpine` | Reverse proxy exposing browserless via `${BROWSERLESS_HOST}` | 80 (HTTP) |

Logs are written to `./logs`, while browserless state (cache, user data, screenshots) persists in `./browserless-data`. Traffic flows through Nginx which proxies to the internal browserless container.

## Getting started

1. Update `.env` with the host name you will expose publicly (`BROWSERLESS_HOST`) and tweak concurrency limits if needed.
2. Start browserless:

   ```powershell
   docker compose up -d
   ```

3. Verify the service is healthy:

   ```powershell
   docker compose ps
   docker compose logs -f browserless
   ```

4. Hit the API at <http://selenium.nhi.co.id/> (or the hostname you configured) to see the status JSON.

> **Note:** The stack now includes an Nginx reverse proxy listening on port 80, which routes all traffic to the browserless container. Direct access to browserless ports is not exposed to the host; instead, use the hostname defined in `BROWSERLESS_HOST`.

## Using browserless from your code

### Selenium (Python example)

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-gpu")

driver = webdriver.Remote(
    command_executor="http://selenium.nhi.co.id/webdriver",
    options=options,
)
driver.get("https://example.com")
print(driver.title)
driver.quit()
```

If you set `BROWSERLESS_TOKEN`, add:

```python
options.set_capability("browserless:token", "your-token")
```

### Playwright / Puppeteer

Browserless also exposes the standard `/playwright` and `/puppeteer` endpoints. Example with Node.js and Playwright:

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connectOverCDP('ws://selenium.nhi.co.id');
const context = await browser.newContext();
const page = await context.newPage();
await page.goto('https://example.com');
console.log(await page.title());
await browser.close();
```

## Configuration reference

Key environment variables live in `.env`:

- `BROWSERLESS_TAG` — docker image tag, e.g. `latest` or a pinned version.
- `BROWSERLESS_HOST` — host name you expose to clients (`selenium.nhi.co.id`).
- `BROWSERLESS_PORT` / `BROWSERLESS_DEBUG_PORT` — forwarded ports for the HTTP API and DevTools protocol.
- `BROWSERLESS_MAX_CONCURRENT` — maximum parallel sessions before queueing.
- `BROWSERLESS_QUEUE_LENGTH` — how many queued sessions are allowed.
- `BROWSERLESS_PREBOOT` — whether to keep Chrome warm for faster cold starts.
- `BROWSERLESS_REFRESH_INTERVAL` — milliseconds before Chrome instances are recycled.
- `BROWSERLESS_ENABLE_DEBUGGER` — allow the live debugger UI.
- `BROWSERLESS_BLOCK_ADS` — enable built-in ad/tracker blocking.
- `BROWSERLESS_TOKEN` — optional API token; leave blank to disable auth.
- `BROWSERLESS_SCREEN_*` — default viewport dimensions.
- `GRID_NETWORK` — compose network name (defaults to `browserless`).

## Smoke test

A Python smoke test lives in `tests/ping_grid.py`. It now targets browserless' WebDriver bridge:

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tests\ping_grid.py
```

Set `BROWSERLESS_WEBDRIVER_URL` or `BROWSERLESS_TOKEN` in your shell before running if you use non-defaults.

## CI pointers

- Run `docker compose pull` during CI setup to ensure the image is cached.
- Persist `logs/` and `browserless-data/` as artifacts if you need post-mortem analysis (screenshots, traces, etc.).
- Tune `BROWSERLESS_MAX_CONCURRENT` per CI runner capacity to avoid timeouts.

## Troubleshooting

- **HTTP 401 errors**: set the `TOKEN` environment variable in `docker-compose.yml` or remove `BROWSERLESS_TOKEN` if you don't want auth.
- **Sessions queued too long**: increase `BROWSERLESS_MAX_CONCURRENT` or reduce suite parallelism.
- **DevTools/WebSocket failures**: ensure port `${BROWSERLESS_DEBUG_PORT}` is reachable from your network.
