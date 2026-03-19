import allure
import pytest

from automation.pages.status_tag_page import StatusTagStoryPage
from automation.tools.asserts import Asserts


@allure.title('StatusTag: размер s имеет высоту 16 ± 2 px')
@pytest.mark.component
def test_status_tag_size_s_has_expected_height_with_tolerance(page, common_test_data):
    story = StatusTagStoryPage(page, common_test_data.URL_STAND, common_test_data.TIMEOUT_MS)
    asserts = Asserts()

    story.open()
    story.select_size_s()

    story.should_size_s_be_checked()
    story.should_status_tag_be_visible()

    actual_height = story.get_status_tag_height()
    asserts.in_range(
        actual=actual_height,
        expected=16,
        tolerance=2,
        text_error=f'Ожидалась высота 16 ± 2 px, но получено {actual_height}px',
    )


@allure.title('StatusTag: размер m имеет высоту 20 ± 2 px')
@pytest.mark.component
def test_status_tag_size_m_has_expected_height_with_tolerance(page, common_test_data):
    story = StatusTagStoryPage(page, common_test_data.URL_STAND, common_test_data.TIMEOUT_MS)
    asserts = Asserts()

    story.open()
    story.select_size_m()

    story.should_size_m_be_checked()
    story.should_status_tag_be_visible()

    actual_height = story.get_status_tag_height()
    asserts.in_range(
        actual=actual_height,
        expected=20,
        tolerance=2,
        text_error=f'Ожидалась высота 20 ± 2 px, но получено {actual_height}px',
    )
