import json
from typing import Optional

import pandas as pd
import datetime


def get_expenses_for_3_months_by_category(operation: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по категории за последние 3 месяца"""
    if operation is None:
        raise ValueError('Транзакции не переданы')
    elif not isinstance(operation, pd.DataFrame):
        raise TypeError('Транзакции должны быть переданы в виде pandas DataFrame')

    if category is None:
        raise ValueError('Категория не передана')
    elif not isinstance(category, str):
        raise TypeError('Категория должна быть передана в виде str')

    if date is None:
        date_obj = datetime.datetime.now()
    else:
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        except ValueError:
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
