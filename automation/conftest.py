from __future__ import annotations

import allure
import pytest
from playwright.sync_api import sync_playwright

from automation.config.config import Config, CommonTestData
from automation.core.artifacts import Artifacts
from automation.core.browser import BrowserFactory
from automation.tools.logger import Logger


class CommonData:
    browsers = {
        'Chromium': 'chromium',
        'Firefox': 'firefox',
        'Webkit': 'webkit',
    }
    browser_name = Config.DEFAULT_BROWSER
    headless = Config.DEFAULT_HEADLESS
    timeout_ms = Config.DEFAULT_TIMEOUT_MS


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default=CommonData.browser_name)
    parser.addoption('--base-url', action='store', default=None)
    parser.addoption('--headed', action='store_true', default=False)
    parser.addoption('--timeout-ms', action='store', default=None)


def set_var_from_args(request) -> CommonTestData:
    defaults = Config.load()
    browser_name = request.config.getoption('browser_name') or defaults.BROWSER_NAME
    base_url = request.config.getoption('base_url') or defaults.URL_STAND
    headed = request.config.getoption('headed')
    timeout_arg = request.config.getoption('timeout_ms')
    timeout_ms = int(timeout_arg) if timeout_arg else defaults.TIMEOUT_MS
    return CommonTestData(
        URL_STAND=base_url,
        BROWSER_NAME=browser_name,
        HEADLESS=not headed if headed else defaults.HEADLESS,
        TIMEOUT_MS=timeout_ms,
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture(scope='session')
def common_test_data(pytestconfig) -> CommonTestData:
    return set_var_from_args(type('RequestLike', (), {'config': pytestconfig})())


@pytest.fixture(scope='session')
def playwright_instance():
    Logger.setup_logger()
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope='session')
def browser(playwright_instance, common_test_data):
    browser = BrowserFactory.build(
        playwright=playwright_instance,
        browser_name=common_test_data.BROWSER_NAME,
        headless=common_test_data.HEADLESS,
    )
    yield browser
    browser.close()


@pytest.fixture(scope='function')
def page(browser, common_test_data, request):
    Logger.clear()
    context = browser.new_context(viewport={'width': 1600, 'height': 1200})
    context.set_default_timeout(common_test_data.TIMEOUT_MS)
    page = context.new_page()
    artifacts = Artifacts(page, request.node.nodeid)

    yield page

    logs_text = Logger.get_from_logger()
    logs_path = artifacts.write_text('logs', logs_text)
    allure.attach(logs_text, 'logs', allure.attachment_type.TEXT)
    allure.attach.file(str(logs_path), name='logs-file', attachment_type=allure.attachment_type.TEXT)

    rep_call = getattr(request.node, 'rep_call', None)
    screenshot_name = 'passed-screenshot'
    if rep_call and rep_call.failed:
        screenshot_name = 'failure-screenshot'
    elif rep_call and rep_call.skipped:
        screenshot_name = 'skipped-screenshot'

    screenshot_path = artifacts.screenshot('final')
    allure.attach.file(
        str(screenshot_path),
        name=screenshot_name,
        attachment_type=allure.attachment_type.PNG,
    )

    context.close()
