import json
from unittest.mock import patch

import pytest

from src.services import filter_transaction_by_search_str


def test_get_transaction_for_filter_transaction_by_search_str(get_data_for_services):
    """Тестирует возврат отфильтрованных операций по строке поиска"""
    result = filter_transaction_by_search_str(get_data_for_services, "МА")

    assert json.loads(result) == [
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
            "Описание": "Колхоз",
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
            "Категория": "Различные товары",
            "MCC": 5411,
            "Описание": "Магнит",
            "Бонусы (включая кэшбэк)": 3.00,
            "Округление на инвесткопилку": 0.0,
            "Сумма операции с округлением": 160.89,
        },
    ]


def test_transactions_not_found_for_filter_transaction_by_search_str(get_data_for_services):
    """Тестирует кейс, когда транзакции не найдены"""
    result = filter_transaction_by_search_str(get_data_for_services, ".")

    assert json.loads(result) == []


def test_none_search_str_for_filter_transaction_by_search_str(get_data_for_services):
    """Тестирует кейс, когда не передана строка поиска"""
    with pytest.raises(ValueError) as exc_info:
        filter_transaction_by_search_str(get_data_for_services, None)
    assert str(exc_info.value) == "Строка для поиска не передана"


def test_search_is_not_str_for_filter_transaction_by_search_str(get_data_for_services):
    """Тестирует кейс, когда cтрока передана не в типе str"""
    with pytest.raises(TypeError) as exc_info:
        filter_transaction_by_search_str(get_data_for_services, ["МА"])
    assert str(exc_info.value) == "Строка передана не в типе str"
