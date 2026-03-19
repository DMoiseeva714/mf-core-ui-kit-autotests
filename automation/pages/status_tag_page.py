from __future__ import annotations

from playwright.sync_api import Locator, Page, FrameLocator, expect

from automation.pages.storybook_page import StorybookPage


class StatusTagStoryPage(StorybookPage):
    STORY_PATH = '?path=/story/компоненты-statustag--status-tag-story'

    def __init__(self, page: Page, base_url: str, timeout_ms: int) -> None:
        super().__init__(page, base_url, timeout_ms)

    # =========================
    # Navigation
    # =========================

    def open(self) -> None:
        self.open_story(self.STORY_PATH)
        self.page.wait_for_load_state('networkidle')

    # =========================
    # Main page / docs controls
    # =========================

    @property
    def color_select(self) -> Locator:
        """
        Color control находится в основном DOM docs/storybook страницы.
        По скриншоту это native select:
        <select id="control-color" ...>
        """
        return self.page.locator('select#control-color').first

    @property
    def size_radio_s(self) -> Locator:
        return self.page.get_by_role('radio', name='s')

    @property
    def size_radio_m(self) -> Locator:
        return self.page.get_by_role('radio', name='m')

    @property
    def label_input(self) -> Locator:
        """
        Label control находится в основном DOM.
        Оставляем универсально: сначала textarea, потом text input.
        """
        textarea = self.page.locator('textarea')
        if textarea.count() > 0:
            return textarea.first

        return self.page.locator('input[type="text"]').first

    # =========================
    # Preview iframe
    # =========================

    @property
    def preview_frame(self) -> FrameLocator:
        """
        Компонент StatusTag рендерится внутри iframe Storybook preview.
        Если понадобится, потом можно сузить до конкретного iframe id.
        """
        return self.page.frame_locator('iframe')

    @property
    def status_tag_root(self) -> Locator:
        """
        Корневой элемент самого компонента внутри iframe.
        """
        return self.preview_frame.locator('div.mf-core-status-tag').first

    @property
    def status_tag_label(self) -> Locator:
        """
        Текст внутри StatusTag.
        """
        return self.status_tag_root.locator('p.mf-core-typography').first

    # =========================
    # Assertions
    # =========================

    def should_be_opened(self) -> None:
        expect(self.status_tag_root).to_be_visible(timeout=self.timeout_ms)

    def should_status_tag_be_visible(self) -> None:
        expect(self.status_tag_root).to_be_visible(timeout=self.timeout_ms)
        expect(self.status_tag_label).to_be_visible(timeout=self.timeout_ms)

    def should_have_label(self, expected_text: str) -> None:
        expect(self.status_tag_label).to_have_text(expected_text, timeout=self.timeout_ms)

    def should_size_s_be_checked(self) -> None:
        expect(self.size_radio_s).to_be_checked(timeout=self.timeout_ms)

    def should_size_m_be_checked(self) -> None:
        expect(self.size_radio_m).to_be_checked(timeout=self.timeout_ms)

    def should_have_background_image_attr(self, expected_attr: str) -> None:
        actual = self.get_background_image_attr()
        assert actual == expected_attr, (
            f"Ожидался data-background-image='{expected_attr}', "
            f"но получено '{actual}'"
        )

    def should_have_height_with_tolerance(
        self,
        expected_height: float,
        tolerance: float = 2.0,
    ) -> None:
        actual_height = self.get_status_tag_height()
        lower = expected_height - tolerance
        upper = expected_height + tolerance

        assert lower <= actual_height <= upper, (
            f'Ожидалась высота в диапазоне [{lower}, {upper}] px, '
            f'но фактическая высота = {actual_height}px'
        )

    # =========================
    # Actions
    # =========================

    def select_color(self, color_value: str) -> None:
        """
        Color control — обычный <select>, поэтому используем select_option.
        """
        self.color_select.select_option(value=color_value)

    def select_size_s(self) -> None:
        self.size_radio_s.check()

    def select_size_m(self) -> None:
        self.size_radio_m.check()

    def fill_label(self, text: str) -> None:
        self.label_input.fill(text)

    # =========================
    # Data getters
    # =========================

    def get_status_tag_height(self) -> float:
        box = self.status_tag_root.bounding_box()
        if box is None:
            raise AssertionError('Не удалось получить bounding_box для StatusTag')
        return box['height']

    def get_background_image_attr(self) -> str | None:
        return self.status_tag_root.get_attribute('data-background-image')

    def get_label_text(self) -> str:
        return self.status_tag_label.inner_text().strip()
