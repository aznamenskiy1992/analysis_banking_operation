import pytest

from unittest.mock import patch, MagicMock

import requests

from src.utils import get_expenses, get_income, get_currency_rates, get_stock_prices


def test_get_expenses_for_get_expenses(get_data_for_get_expenses):
    """Тестирует возврат расходов"""
    result = get_expenses(
        get_data_for_get_expenses
    )

    assert result == {
        "expenses": {
            "total_amount": 16613,
            "main": [
                {
                    "category": "Дом и ремонт",
                    "amount": 3250
                },
                {
                    "category": "Супермаркеты",
                    "amount": 681
                },
                {
                    "category": "Ж/д билеты",
                    "amount": 330
                },
                {
                    "category": "Фастфуд",
                    "amount": 296
                },
                {
                    "category": "Связь",
                    "amount": 225
                },
                {
                    "category": "Каршеринг",
                    "amount": 170
                },
                {
                    "category": "Различные товары",
                    "amount": 150
                },
                {
                    "category": "Остальное",
                    "amount": 260
                },
            ],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": 8000
                },
                {
                    "category": "Переводы",
                    "amount": 3250
                },
            ],
        }
    }


def test_not_have_expenses_for_get_expenses(get_data_for_get_expenses):
    """Тестирует кейс, когда нет расходов"""
    result = get_expenses(
        get_data_for_get_expenses[-4:]
    )

    assert result == {
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
                },
            ],
        }
    }


def test_less_7_categories_for_get_expenses(get_data_for_get_expenses):
    """Тестирует кейс, когда меньше 7 категорий"""
    result = get_expenses(
        get_data_for_get_expenses[-6:]
    )

    assert result == {
        "expenses": {
            "total_amount": 11595,
            "main": [
                {
                    "category": "Связь",
                    "amount": 225
                },
                {
                    "category": "Цветы",
                    "amount": 120
                },
            ],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": 8000
                },
                {
                    "category": "Переводы",
                    "amount": 3250
                },
            ],
        }
    }


def test_not_have_cash_category_for_get_expenses(get_data_for_get_expenses):
    """Тестирует кейс, когда нет категории наличные"""
    result = get_expenses(
        get_data_for_get_expenses[-2:]
    )

    assert result == {
        "expenses": {
            "total_amount": 3250,
            "main": [],
            "transfers_and_cash": [
                {
                    "category": "Переводы",
                    "amount": 3250
                },
            ],
        }
    }


def test_not_have_transfers_category_for_get_expenses(get_data_for_get_expenses):
    """Тестирует кейс, когда нет категории переводы"""
    result = get_expenses(
        get_data_for_get_expenses[-4:-2]
    )

    assert result == {
        "expenses": {
            "total_amount": 8000,
            "main": [],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": 8000
                },
            ],
        }
    }


def test_not_have_cash_and_transfers_categories_for_get_expenses(get_data_for_get_expenses):
    """Тестирует кейс, когда нет категорий наличные и переводы"""
    result = get_expenses(
        get_data_for_get_expenses[:-4]
    )

    assert result == {
        "expenses": {
            "total_amount": 5363,
            "main": [
                {
                    "category": "Дом и ремонт",
                    "amount": 3250
                },
                {
                    "category": "Супермаркеты",
                    "amount": 681
                },
                {
                    "category": "Ж/д билеты",
                    "amount": 330
                },
                {
                    "category": "Фастфуд",
                    "amount": 296
                },
                {
                    "category": "Связь",
                    "amount": 225
                },
                {
                    "category": "Каршеринг",
                    "amount": 170
                },
                {
                    "category": "Различные товары",
                    "amount": 150
                },
                {
                    "category": "Остальное",
                    "amount": 260
                },
            ],
            "transfers_and_cash": [],
        }
    }


def test_get_income_for_get_income(get_data_for_get_income):
    """Тестирует кейс по возврату поступлений"""
    result = get_income(get_data_for_get_income)

    assert result == {
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
                },
            ]
        }
    }


def test_not_have_income_for_get_income(get_data_for_get_expenses):
    """Тестирует кейс, когда нет поступлений"""
    result = get_income(get_data_for_get_expenses)

    assert result == {
        "income": {
            "total_amount": 0,
            "main": []
        }
    }


@patch('requests.get')
def test_get_currency_rate_for_get_currency_rates(mock_get, get_currency_response_for_get_currency_rates):
    """Тестирует возврат курсов валют"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = get_currency_response_for_get_currency_rates
    mock_get.return_value = mock_response

    result = get_currency_rates(['USD', 'EUR'])

    assert result == {
        "currency_rates": [
            {
                "currency": "USD",
                "rate": 78.918179
            },
            {
                "currency": "EUR",
                "rate": 90.000
            }
        ]
    }

    assert  mock_get.call_count == 2


@pytest.mark.parametrize(
    'input_currencies, raise_message',
    [
        ([], 'Список валют пустой'),
        (None, 'Валюты не переданы',)
    ]
)
def test_incorrect_input_currencies_for_get_currency_rates(input_currencies, raise_message):
    """Тестирует кейсы, когда валюты не переданы или переданы некорректно"""
    with pytest.raises(ValueError) as exc_info:
        get_currency_rates(input_currencies)
    assert str(exc_info.value) == raise_message


def test_currencies_is_not_list_for_get_currency_rates():
    """Тестирует кейс, когда валюты переданы не в списке"""
    with pytest.raises(TypeError) as exc_info:
        get_currency_rates({'USD',})
    assert str(exc_info.value) == 'Валюты переданы не в списке'


@patch('requests.get')
def test_http_error_for_get_currency_rates(mock_get):
    """Тестирует HTTP ошибки при get запросе"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError) as exc_info:
        get_currency_rates(['Доллар'])
    assert 'Ошибка HTTP:' in str(exc_info.value)

    assert mock_get.call_count == 1


@patch('requests.get')
def test_other_error_for_get_currency_rates(mock_get):
    """Тестирует остальные ошибки при get запросе"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Текст ошибки")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.RequestException) as exc_info:
        get_currency_rates(['USD'])
    assert 'Ошибка:' in str(exc_info.value)

    assert mock_get.call_count == 1


@patch('requests.get')
def test_get_stock_prices_for_get_stock_prices(mock_get, get_data_for_get_stock_prices):
    """Тестирует возврат стоимости акций"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = get_data_for_get_stock_prices
    mock_get.return_value = mock_response

    result = get_stock_prices(['AAPL', 'AMZN'])

    assert result == {
        "stock_prices": [
            {
                "stock": "AAPL",
                "price": 213.55
            },
            {
                "stock": "AMZN",
                "price": 320.55
            },
        ]
    }

    mock_get.assert_called_once()


@pytest.mark.parametrize(
    'input_stocks, raise_message',
    [
        ([], 'Список акций пустой'),
        (None, 'Акции не переданы',)
    ]
)
def test_incorrect_input_stocks_for_get_stock_prices(input_stocks, raise_message):
    """Тестирует кейсы, когда акции не переданы или переданы некорректно"""
    with pytest.raises(ValueError) as exc_info:
        get_stock_prices(input_stocks)
    assert str(exc_info.value) == raise_message


def test_stocks_is_not_list_for_get_stock_prices():
    """Тестирует кейс, когда акции переданы не в списке"""
    with pytest.raises(TypeError) as exc_info:
        get_stock_prices({'AMZN',})
    assert str(exc_info.value) == 'Акции переданы не в списке'


@patch('requests.get')
def test_http_error_for_get_stock_prices(mock_get):
    """Тестирует HTTP ошибки при get запросе"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError) as exc_info:
        get_stock_prices(['АМЗН'])
    assert 'Ошибка HTTP:' in str(exc_info.value)

    assert mock_get.call_count == 1
