from __future__ import annotations

from playwright.sync_api import expect


class Wait:
    def __init__(self, timeout_ms: int) -> None:
        self.timeout_ms = timeout_ms

    def visible(self, locator):
        expect(locator).to_be_visible(timeout=self.timeout_ms)

    def hidden(self, locator):
        expect(locator).to_be_hidden(timeout=self.timeout_ms)
