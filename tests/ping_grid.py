"""Minimal end-to-end smoke test for the Selenium Grid stack."""

from __future__ import annotations

import os
import sys
from contextlib import suppress
from time import perf_counter

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


GRID_URL = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444/wd/hub")
TARGET_URL = os.getenv("TEST_TARGET_URL", "https://example.com")
WAIT_SECONDS = int(os.getenv("TEST_WAIT_SECONDS", "30"))


def main() -> int:
    start = perf_counter()
    options = ChromeOptions()
    options.set_capability("se:recordVideo", True)
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")

    try:
        with webdriver.Remote(command_executor=GRID_URL, options=options) as driver:
            driver.get(TARGET_URL)
            wait = WebDriverWait(driver, WAIT_SECONDS)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            title = driver.title
    except WebDriverException as exc:  # pragma: no cover - CLI feedback only
        print(f"[ERROR] WebDriver failed: {exc}", file=sys.stderr)
        return 1

    duration = perf_counter() - start
    print(f"Grid responded with page '{title}' in {duration:.2f}s via {GRID_URL}")
    return 0


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        sys.exit(main())
