from textwrap import indent

import pytest
import json

from unittest.mock import patch
import pandas as pd

from src.views import get_events


@patch('src.views.get_stock_prices')
@patch('src.views.get_currency_rates')
@patch('src.views.get_income')
@patch('src.views.get_expenses')
def test_get_result_inner_function_for_get_events(mock_get_expenses, mock_get_income, mock_get_currency_rates, mock_get_stock_prices, result_inner_functions_for_get_events):
    """Тестирует возврат результатов от внутренних функций"""
    mock_get_expenses.return_value = result_inner_functions_for_get_events['get_expenses']
    mock_get_income.return_value = result_inner_functions_for_get_events['get_income']
    mock_get_currency_rates.return_value = result_inner_functions_for_get_events['get_currency_rates']
    mock_get_stock_prices.return_value = result_inner_functions_for_get_events['get_stock_prices']

    result = get_events(pd.DataFrame([{'test': 'test'}, {'test': 'test'}]), '2025-07-05')

    assert json.loads(result) == {
        "expenses": {
            "total_amount": 11250,
            "main": [],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": 8000
                },
                {
                    "category": "Переводы",
                    "amount": 3250
                }
            ]
        },
        "income": {
            "total_amount": 9200,
            "main": [
                {
                    "category": "Пополнение через Газпромбанк",
                    "amount": 8000
                },
                {
                    "category": "Пополнение через Сбер",
                    "amount": 1200
                }
            ]
        },
        "currency_rates": [
            {
                "currency": "USD",
                "rate": 78.918179
            },
            {
                "currency": "EUR",
                "rate": 90.000
            }
        ],
        "stock_prices": [
            {
                "stock": "AAPL",
                "price": 213.55
            },
            {
                "stock": "AMZN",
                "price": 320.55
            }
        ]
    }


@pytest.mark.parametrize(
    'date_, raise_message',
    [
        (None, 'Дата не передана'),
        ('2025 07 07', 'Дата указана неверно. Маска: YYYY-MM-DD')
    ]
)
def test_incorrect_date_for_get_events(date_, raise_message):
    """Тестирует кейс, когда дата не передана или не конвертируется в datetime"""
    with pytest.raises(ValueError) as exc_info:
        get_events(pd.DataFrame([{'test': 'test'}, {'test': 'test'}]), date_)

    assert str(exc_info.value) == raise_message
