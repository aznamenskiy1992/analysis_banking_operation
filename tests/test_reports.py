import pandas as pd
import pytest
from unittest.mock import patch
import datetime
import json

from src.reports import get_expenses_for_3_months_by_category


def test_get_expenses_for_get_expenses_for_3_months_by_category(get_data_for_reports):
    """Тестирует возврат трат за 3 месяца по категории"""

    result = get_expenses_for_3_months_by_category(get_data_for_reports, 'Супермаркеты', '2021-12-31')

    assert json.loads(result) == [
        {
            "Категория": "Супермаркеты",
            "Сумма операции с округлением": 321.78,
        },
    ]


def test_none_expenses_for_get_expenses_for_3_months_by_category(get_data_for_reports):
    """Тестирует кейс, когда по категории не было трат"""

    result = get_expenses_for_3_months_by_category(get_data_for_reports, 'Переводы', '2021-12-31')

    assert json.loads(result) == []


def test_none_operation_for_get_expenses_for_3_months_by_category():
    """Тестирует кейс, когда транзакции не переданы"""
    with pytest.raises(ValueError) as exc_info:
        get_expenses_for_3_months_by_category(None, 'Переводы', '2021-12-31')
    assert str(exc_info.value) == "Транзакции не переданы"
