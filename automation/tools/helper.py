from __future__ import annotations

from pathlib import Path
from playwright.sync_api import Page


class Screenshot:
    def __init__(self, page: Page) -> None:
        self.page = page

    def shot(self, file_path: str) -> Path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path), full_page=True)
        return path
