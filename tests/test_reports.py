import pandas as pd
import pytest
from unittest.mock import patch
import datetime
import json
import logging

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


def test_none_operation_for_get_expenses_for_3_months_by_category(caplog):
    """Тестирует кейс, когда транзакции не переданы"""
    caplog.set_level(logging.DEBUG)

    with pytest.raises(ValueError) as exc_info:
        get_expenses_for_3_months_by_category(None, 'Переводы', '2021-12-31')
    assert str(exc_info.value) == 'Транзакции не переданы'

    assert 'Ошибка: Не переданы транзакции' in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'


def test_operation_is_not_pd_df_for_get_expenses_for_3_months_by_category(caplog):
    """Тестирует кейс, когда транзакции переданы не как pd.DataFrame"""
    caplog.set_level(logging.DEBUG)

    with pytest.raises(TypeError) as exc_info:
        get_expenses_for_3_months_by_category([], 'Переводы', '2021-12-31')
    assert str(exc_info.value) == 'Транзакции должны быть переданы в виде pandas DataFrame'

    assert 'Ошибка: Транзакции переданы в типе' in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'


def test_none_category_for_get_expenses_for_3_months_by_category(get_data_for_reports, caplog):
    """Тестирует кейс, когда категория не передана"""
    caplog.set_level(logging.DEBUG)

    with pytest.raises(ValueError) as exc_info:
        get_expenses_for_3_months_by_category(get_data_for_reports, None, '2021-12-31')
    assert str(exc_info.value) == 'Категория не передана'

    assert 'Ошибка: Категория не передана' in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'


def test_category_is_not_str_for_get_expenses_for_3_months_by_category(get_data_for_reports, caplog):
    """Тестирует кейс, когда категория передана не в str"""
    caplog.set_level(logging.DEBUG)

    with pytest.raises(TypeError) as exc_info:
        get_expenses_for_3_months_by_category(get_data_for_reports, [], '2021-12-31')
    assert str(exc_info.value) == 'Категория должна быть передана в виде str'

    assert 'Ошибка: Категория передана в типе' in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'


def test_date_not_convert_to_datetime_for_get_expenses_for_3_months_by_category(get_data_for_reports, caplog):
    """Тестирует кейс, когда дата не конвертируется в datetime"""
    caplog.set_level(logging.DEBUG)

    with pytest.raises(ValueError) as exc_info:
        get_expenses_for_3_months_by_category(get_data_for_reports, 'Переводы', '31.12.2025')
    assert str(exc_info.value) == 'Дата указана неверно. Маска: YYYY-MM-DD'

    assert "не конвертируется в datetime" in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'


@patch('src.reports.datetime.datetime', wraps=datetime.datetime)
def test_date_is_none_for_get_expenses_for_3_months_by_category(mock_datetime, get_now_data_for_reports):
    """Тестирует кейс, когда дата не передана"""
    mock_datetime.now.return_value = get_now_data_for_reports[0]

    result = get_expenses_for_3_months_by_category(get_now_data_for_reports[-1], 'Супермаркеты')

    assert json.loads(result) == [
        {
            "Категория": "Супермаркеты",
            "Сумма операции с округлением": 160.89,
        },
    ]
