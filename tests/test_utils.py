import pytest

from unittest.mock import patch, MagicMock

from example_api_requests_and_response import result
from src.utils import get_expenses, get_income, get_currency_rates


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
    # Настраиваем mock
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
                "rate": 93.01
            }
        ]
    }

