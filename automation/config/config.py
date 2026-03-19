from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


class Path:
    ROOT_DIR = os.getcwd() + '/'


@dataclass(frozen=True)
class CommonTestData:
    URL_STAND: str
    BROWSER_NAME: str
    HEADLESS: bool
    TIMEOUT_MS: int


class Config:
    DEFAULT_BASE_URL = 'http://ui-kit.mf.work.nxt.bars.group/'
    DEFAULT_BROWSER = 'chromium'
    DEFAULT_HEADLESS = True
    DEFAULT_TIMEOUT_MS = 10000

    @staticmethod
    def load() -> CommonTestData:
        load_dotenv()
        base_url = os.getenv('BASE_URL', Config.DEFAULT_BASE_URL)
        browser = os.getenv('BROWSER', Config.DEFAULT_BROWSER)
        headless_raw = os.getenv('HEADLESS', str(Config.DEFAULT_HEADLESS))
        timeout_ms = int(os.getenv('TIMEOUT_MS', str(Config.DEFAULT_TIMEOUT_MS)))
        headless = headless_raw.strip().lower() in {'1', 'true', 'yes', 'on'}
        return CommonTestData(
            URL_STAND=base_url,
            BROWSER_NAME=browser,
            HEADLESS=headless,
            TIMEOUT_MS=timeout_ms,
        )
