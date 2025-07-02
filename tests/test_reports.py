import pandas as pd
import pytest
from unittest.mock import patch
import datetime

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

    assert result == pd.DataFrame(
        [
            {
                "Дата операции": "28.12.2021 16:44:00",
                "Дата платежа": "31.12.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": "-160,89",
                "Валюта операции": "RUB",
                "Сумма платежа": "-160,89",
                "Валюта платежа": "RUB",
                "Кэшбэк": 0,
                "Категория": "Супермаркеты",
                "MCC": 5411,
                "Описание": "Магнит",
                "Бонусы (включая кэшбэк)": 3.00,
                "Округление на инвесткопилку": 0.0,
                "Сумма операции с округлением": 160.89,
            },
            {
                "Дата операции": "31.12.2021 16:44:00",
                "Дата платежа": "31.12.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": "-160,89",
                "Валюта операции": "RUB",
                "Сумма платежа": "-160,89",
                "Валюта платежа": "RUB",
                "Кэшбэк": 0,
                "Категория": "Супермаркеты",
                "MCC": 5411,
                "Описание": "Магнит",
                "Бонусы (включая кэшбэк)": 3.00,
                "Округление на инвесткопилку": 0.0,
                "Сумма операции с округлением": 160.89,
            },
        ]
    )
