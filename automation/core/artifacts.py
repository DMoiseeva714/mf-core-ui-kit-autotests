from __future__ import annotations

import hashlib
import re
from pathlib import Path

from playwright.sync_api import Page


class Artifacts:
    def __init__(self, page: Page, node_name: str) -> None:
        self.page = page
        safe_name = self._make_safe_name(node_name)
        self.base_dir = Path('test-results') / safe_name
        self.base_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _make_safe_name(node_name: str, limit: int = 80) -> str:
        normalized = node_name.encode('ascii', 'backslashreplace').decode('ascii')
        normalized = normalized.replace('::', '__').replace('/', '_').replace('\\', '_')
        normalized = re.sub(r'[^A-Za-z0-9._-]+', '_', normalized).strip('._')
        if not normalized:
            normalized = 'test'
        digest = hashlib.sha1(node_name.encode('utf-8')).hexdigest()[:10]
        shortened = normalized[:limit].rstrip('._')
        return f'{shortened}_{digest}'

    def screenshot(self, name: str = 'screen') -> Path:
        path = self.base_dir / f'{name}.png'
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path), full_page=True)
        return path

    def write_text(self, name: str, content: str, suffix: str = '.txt') -> Path:
        path = self.base_dir / f'{name}{suffix}'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path
