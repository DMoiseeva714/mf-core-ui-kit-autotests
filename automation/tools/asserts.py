from __future__ import annotations

import allure


class Asserts:
    def compare(
        self,
        variable_first,
        comparison_sign: str,
        variable_second,
        text_error: str,
    ):
        with allure.step(
            f'Assertion: comparing "{variable_first}" {comparison_sign} "{variable_second}"'
        ):
            if comparison_sign in ('=', '=='):
                assert variable_first == variable_second, text_error
            elif comparison_sign == '!=':
                assert variable_first != variable_second, text_error
            elif comparison_sign == '>':
                assert variable_first > variable_second, text_error
            elif comparison_sign == '<':
                assert variable_first < variable_second, text_error
            elif comparison_sign == '>=':
                assert variable_first >= variable_second, text_error
            elif comparison_sign == '<=':
                assert variable_first <= variable_second, text_error
            elif comparison_sign == 'in':
                assert variable_first in variable_second, text_error
            else:
                raise ValueError(f'Unknown comparison sign {comparison_sign}')

    def in_range(self, actual: float, expected: float, tolerance: float, text_error: str):
        with allure.step(
            f'Assertion: value {actual} in range [{expected - tolerance}, {expected + tolerance}]'
        ):
            assert expected - tolerance <= actual <= expected + tolerance, text_error
