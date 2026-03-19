import allure
import pytest

from automation.pages.status_tag_page import StatusTagStoryPage


@allure.title('StatusTag: ручное изменение label')
@pytest.mark.component
@pytest.mark.parametrize('custom_label', ['новый статус', 'тестовый тег', 'ожидает проверки'])
def test_status_tag_manual_label_change(page, common_test_data, custom_label: str):
    story = StatusTagStoryPage(page, common_test_data.URL_STAND, common_test_data.TIMEOUT_MS)

    story.open()
    story.fill_label(custom_label)

    story.should_status_tag_be_visible()
    story.should_have_label(custom_label)
