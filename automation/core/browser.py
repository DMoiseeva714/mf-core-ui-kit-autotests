from __future__ import annotations

from playwright.sync_api import Playwright


class BrowserFactory:
    @staticmethod
    def build(playwright: Playwright, browser_name: str, headless: bool):
        browser_type = getattr(playwright, browser_name)
        return browser_type.launch(headless=headless)
