import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import get_events


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.get_income")
@patch("src.views.get_expenses")
def test_get_result_inner_function_for_get_events(
    mock_get_expenses,
    mock_get_income,
    mock_get_currency_rates,
    mock_get_stock_prices,
    result_inner_functions_for_get_events,
):
    """Тестирует возврат результатов от внутренних функций"""
    mock_get_expenses.return_value = result_inner_functions_for_get_events["get_expenses"]
    mock_get_income.return_value = result_inner_functions_for_get_events["get_income"]
    mock_get_currency_rates.return_value = result_inner_functions_for_get_events["get_currency_rates"]
    mock_get_stock_prices.return_value = result_inner_functions_for_get_events["get_stock_prices"]

    result = get_events(
        pd.DataFrame(
            [{"test": "test", "Дата операции": "2025-05-07"}, {"test": "test", "Дата операции": "2025-05-07"}]
        ),
        "2025-07-05",
    )

    assert json.loads(result) == {
        "expenses": {
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": [],
        },
        "income": {
            "total_amount": 0,
            "main": [],
        },
        "currency_rates": [{"currency": "USD", "rate": 78.918179}],
        "stock_prices": [{"stock": "AAPL", "price": 213.55}],
    }


@pytest.mark.parametrize(
    "date_, raise_message", [(None, "Дата не передана"), ("2025 07 07", "Дата указана неверно. Маска: YYYY-MM-DD")]
)
def test_incorrect_date_for_get_events(date_, raise_message):
    """Тестирует кейс, когда дата не передана или не конвертируется в datetime"""
    with pytest.raises(ValueError) as exc_info:
        get_events(pd.DataFrame([{"test": "test"}, {"test": "test"}]), date_)

    assert str(exc_info.value) == raise_message
