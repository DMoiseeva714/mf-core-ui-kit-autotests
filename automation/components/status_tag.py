from __future__ import annotations

from playwright.sync_api import Locator


class StatusTagComponent:
    def __init__(self, root: Locator) -> None:
        self.root = root

    @property
    def label(self) -> Locator:
        return self.root.locator('p.mf-core-typography').first

    def height(self) -> float:
        box = self.root.bounding_box()
        if box is None:
            raise AssertionError('StatusTag bounding_box is None')
        return box['height']

    def background_image(self) -> str | None:
        return self.root.get_attribute('data-background-image')
