# Browserless Automation Stack (Plesk-Optimized)

This project packages [browserless](https://www.browserless.io/) via Docker Compose for automation, scraping, or testing with headless Chrome. It's designed to work seamlessly with **Plesk Docker Proxy Rules** so you don't need an additional Nginx container.

## Requirements

- Docker Desktop 4.0+ with Compose V2 (`docker compose` command), or **Plesk with Docker support**
- Roughly 2 GB of free RAM per concurrent Chrome session (adjust via `.env`)

## What's inside

| Service | Image | Purpose | Ports |
| --- | --- | --- | --- |
| `browserless` | `browserless/chrome:${BROWSERLESS_TAG}` | Headless Chrome runtime with browserless API & WebDriver bridge | `${BROWSERLESS_PORT}` (default 3000) |

Logs are written to `./logs`, while browserless state (cache, user data, screenshots) persists in `./browserless-data`.

## Getting started

### Option A: Plesk Docker Proxy (Recommended)

1. Update `.env` with your settings (especially `BROWSERLESS_TOKEN` for security).
2. In Plesk, go to **Docker** → Deploy your compose stack.
3. After the container starts, go to **Domains** → your domain → **Apache & Nginx Settings** → **Additional nginx directives** and add:

   ```nginx
   location / {
       proxy_pass http://127.0.0.1:3000;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_read_timeout 300s;
   }
   ```

4. Click **OK** and **Apply**. Now `http://selenium.nhi.co.id/` will proxy to the browserless container on port 3000.

### Option B: Manual Docker Compose

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

4. Hit the API at <http://selenium.nhi.co.id/> (if using Plesk proxy) or <http://localhost:3000/> (direct access) to see the status JSON.

## Using browserless from your code

### Selenium (Python example)

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-gpu")
options.set_capability("browserless:token", "xmH3Xg1mYkIqX1Yj")

driver = webdriver.Remote(
    command_executor="http://selenium.nhi.co.id/webdriver",
    options=options,
)
driver.get("https://example.com")
print(driver.title)
driver.quit()
```

> Use your actual hostname and adjust the token if you changed `BROWSERLESS_TOKEN` in `.env`.

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
- `BROWSERLESS_PORT` — container port to publish on the host (default `3000`).
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
