from __future__ import annotations

import time
import traceback


class Logger:
    _TEXT_LOGGER = ''
    _COUNTER = 0
    _TIME_START = time.time()

    @classmethod
    def setup_logger(cls):
        cls._TEXT_LOGGER = ''
        cls._COUNTER = 0
        cls._TIME_START = time.time()

    @classmethod
    def clear(cls):
        cls.setup_logger()

    @classmethod
    def get_from_logger(cls) -> str:
        return cls._TEXT_LOGGER

    @classmethod
    def record(cls, text: str = '', **kwargs):
        tb = traceback.format_stack(limit=4)
        cls._COUNTER += 1
        elapsed = round((time.time() - cls._TIME_START), 2)
        cls._TEXT_LOGGER += f'<{cls._COUNTER}><time {elapsed} s>-------------------\n'
        cls._TEXT_LOGGER += f'description -> {text}\n'
        if 'data' in kwargs:
            cls._TEXT_LOGGER += f'data -> {kwargs["data"]}\n'
        cls._TEXT_LOGGER += f'traceback -> {tb[-2]}\n'
