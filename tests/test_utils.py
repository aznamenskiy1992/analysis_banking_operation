import pytest

from src.utils import get_expenses


def test_get_expenses_for_get_expenses(get_data_for_get_expenses):
    """Тестирует возврат расходов"""
    result = get_expenses(
        get_data_for_get_expenses
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
            "total_amount": 0,
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
            "total_amount": 345,
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
            "total_amount": 0,
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
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": 8000
                },
            ],
        }
    }
