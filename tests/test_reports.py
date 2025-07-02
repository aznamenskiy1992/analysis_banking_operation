import pandas as pd
import pytest
from unittest.mock import patch
import datetime
import json

from src.reports import get_expenses_for_3_months_by_category


@patch('datetime.now')
@pytest.mark.parametrize(
    'date_',
    [ '2020,12,31', None]
)
def test_get_expenses_for_get_expenses_for_3_months_by_category(mock_now_date, date_, get_data_for_reports):
    """Тестирует возврат трат за 3 месяца по категории"""
    mock_now_date = datetime.datetime(2021, 12, 31, 16, 44, 00)

    result = get_expenses_for_3_months_by_category(get_data_for_reports, 'Супермаркеты', date_)

    assert json.loads(result) == [
        {
            "Супермаркеты": 321.78,
        },
    ]
