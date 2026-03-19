import allure
import pytest

from automation.pages.status_tag_page import StatusTagStoryPage


@allure.title('StatusTag: story открывается')
@pytest.mark.component
@pytest.mark.smoke
def test_status_tag_story_is_opened(page, common_test_data):
    story = StatusTagStoryPage(page, common_test_data.URL_STAND, common_test_data.TIMEOUT_MS)

    story.open()

    story.should_be_opened()


@allure.title('StatusTag: компонент отображается')
@pytest.mark.component
def test_status_tag_is_visible(page, common_test_data):
    story = StatusTagStoryPage(page, common_test_data.URL_STAND, common_test_data.TIMEOUT_MS)

    story.open()

    story.should_status_tag_be_visible()


@allure.title('StatusTag: дефолтный label = черновик')
@pytest.mark.component
def test_status_tag_default_label_is_chernovik(page, common_test_data):
    story = StatusTagStoryPage(page, common_test_data.URL_STAND, common_test_data.TIMEOUT_MS)

    story.open()

    story.should_have_label('черновик')
