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
