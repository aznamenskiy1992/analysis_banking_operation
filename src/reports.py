import json
from typing import Optional
import logging

import pandas as pd
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def get_expenses_for_3_months_by_category(operation: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по категории за последние 3 месяца"""
    if operation is None:
        logger.critical('Ошибка: Не переданы транзакции')
        raise ValueError('Транзакции не переданы')
    elif not isinstance(operation, pd.DataFrame):
        logger.critical(f'Ошибка: Транзакции переданы в типе {type(operation)}')
        raise TypeError('Транзакции должны быть переданы в виде pandas DataFrame')

    if category is None:
        logger.critical('Ошибка: Категория не передана')
        raise ValueError('Категория не передана')
    elif not isinstance(category, str):
        logger.critical(f'Ошибка: Категория передана в типе {type(category)}')
        raise TypeError('Категория должна быть передана в виде str')

    if date is None:
        date_obj = datetime.datetime.now()
    else:
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        except ValueError:
            logger.critical(f'Ошибка: Дата ({date, type(date)}) не конвертируется в datetime')
            raise ValueError('Дата указана неверно. Маска: YYYY-MM-DD')

    if not pd.api.types.is_datetime64_dtype(operation['Дата операции']):
        operation['Дата операции'] = pd.to_datetime(operation['Дата операции'], dayfirst=True)

    normalize_category: str = category.strip().capitalize()

    start_date = date_obj - datetime.timedelta(days=90)

    filtered_operation = operation.loc[
        (operation['Дата операции'].notnull()) &
        (operation['Категория'].notnull()) &
        (operation['Категория'] == normalize_category) &
        (operation['Дата операции'] >= start_date) &
        (operation['Дата операции'] <= date_obj)
    ]

    if len(filtered_operation) != 0:
        grouped_operation = filtered_operation.groupby('Категория')['Сумма операции с округлением'].sum().reset_index()
        return json.dumps(grouped_operation.to_dict(orient='records'))
    else:
        return json.dumps([])
