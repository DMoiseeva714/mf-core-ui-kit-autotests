from __future__ import annotations

from playwright.sync_api import Page

from automation.tools.logger import Logger
from automation.tools.wait import Wait


class BasePage:
    def __init__(self, page: Page, base_url: str, timeout_ms: int) -> None:
        self.page = page
        self.base_url = base_url.rstrip('/')
        self.wait = Wait(timeout_ms)
        self.timeout_ms = timeout_ms

    def open_url(self, url: str) -> None:
        Logger.record('Открытие страницы', data=url)
        self.page.goto(url, wait_until='domcontentloaded', timeout=self.timeout_ms)

    def open_path(self, path: str) -> None:
        url = f'{self.base_url}/{path.lstrip("/")}'
        self.open_url(url)
