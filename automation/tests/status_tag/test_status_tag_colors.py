import allure
import pytest

from automation.pages.status_tag_page import StatusTagStoryPage
from automation.tools.asserts import Asserts
from automation.tests.status_tag.data import STATUS_TAG_BACKGROUND_CASES


@allure.title('StatusTag: цвет меняет background атрибут')
@pytest.mark.component
@pytest.mark.parametrize(
    'color_value, expected_background_attr',
    STATUS_TAG_BACKGROUND_CASES,
    ids=[case[0] for case in STATUS_TAG_BACKGROUND_CASES],
)
def test_status_tag_color_changes_background(
    page,
    common_test_data,
    color_value: str,
    expected_background_attr: str,
):
    story = StatusTagStoryPage(
        page,
        common_test_data.URL_STAND,
        common_test_data.TIMEOUT_MS,
    )
    asserts = Asserts()

    story.open()

    story.color_select.wait_for(state='visible', timeout=common_test_data.TIMEOUT_MS)
    story.select_color(color_value)

    story.should_status_tag_be_visible()
    story.should_have_background_image_attr(expected_background_attr)

    actual_background_attr = story.get_background_image_attr()

    asserts.compare(
        actual_background_attr,
        '==',
        expected_background_attr,
        text_error=(
            f"Ожидался data-background-image='{expected_background_attr}', "
            f"но получено '{actual_background_attr}'"
        ),
    )
