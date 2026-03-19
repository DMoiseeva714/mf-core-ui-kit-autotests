from __future__ import annotations

from automation.pages.base_page import BasePage


class StorybookPage(BasePage):
    def open_story(self, story_path: str) -> None:
        self.open_path(story_path)
