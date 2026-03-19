## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python scripts/install_playwright.py
```

## Настройки

Локальный запуск использует `.env` или значения из `automation/config/config.py`.

Пример:

```env
BASE_URL=http://localhost:6006
BROWSER=chromium
HEADLESS=true
TIMEOUT_MS=10000
```

## Запуск тестов

Все тесты StatusTag:

```bash
pytest automation/tests/status_tag
```

С другим адресом Storybook:

```bash
pytest automation/tests/status_tag --base-url http://localhost:5173
```

## Allure

```bash
python -m pytest automation/tests/status_tag --alluredir=allure-results
allure serve allure-results
```

При завершении теста автоматически прикладывается screenshot, а логи прикладываются в Allure для каждого теста.
