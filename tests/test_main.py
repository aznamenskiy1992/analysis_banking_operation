import json

import pytest
from unittest.mock import patch
import pandas as pd

from src.main import main


@patch("builtins.input")
@patch('src.main.get_expenses_for_3_months_by_category')
@patch('src.main.filter_transaction_by_search_str')
@patch('src.main.get_events')
@patch('src.main.get_data')
def test_get_main_data_for_main(mock_get_data, mock_get_events, mock_filter_transaction_by_search_str, mock_get_expenses_for_3_months_by_category, mock_input, result_all_functions_for_main, capsys):
    """Тестирует вывод результата от всех функций программы"""

    mock_get_data.return_value = pd.DataFrame(result_all_functions_for_main['get_data'])
    mock_get_events.return_value = result_all_functions_for_main['get_events']
    mock_filter_transaction_by_search_str.return_value = result_all_functions_for_main['filter_transaction_by_search_str']
    mock_get_expenses_for_3_months_by_category.return_value = result_all_functions_for_main['get_expenses_for_3_months_by_category']

    mock_input.side_effect = [
        '2025-07-07',
        'Y',
        'Супермаркеты',
        'Супермаркеты',
        '2025-07-06'
    ]

    main()

    events_result = '{"expenses": {"total_amount": 11250,"main": [],"transfers_and_cash": [{"category": "Наличные","amount": 8000},{"category": "Переводы","amount": 3250}]},"income": {"total_amount": 9200,"main": [{"category": "Пополнение через Газпромбанк","amount": 8000},{"category": "Пополнение через Сбер","amount": 1200}]},"currency_rates": [{"currency": "USD","rate": 78.918179},{"currency": "EUR","rate": 90.000}],"stock_prices": [{"stock": "AAPL","price": 213.55},{"stock": "AMZN","price": 320.55}]}\n'
    filter_result = '[{"Дата операции": "31.12.2021 16:44:00","Дата платежа": "31.12.2021","Номер карты": "*7197","Статус": "OK","Сумма операции": "-160,89","Валюта операции": "RUB","Сумма платежа": "-160,89","Валюта платежа": "RUB","Кэшбэк": 0,"Категория": "Супермаркеты","MCC": 5411,"Описание": "Колхоз","Бонусы (включая кэшбэк)": 3.00,"Округление на инвесткопилку": 0.0,"Сумма операции с округлением": 160.89}]\n'
    expenses_result = '[{"Категория": "Супермаркеты", "Сумма операции с округлением": 321.78}]\n'

    captured = capsys.readouterr()
    assert  captured.out == events_result + filter_result + expenses_result
