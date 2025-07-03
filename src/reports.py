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

    if date is None:
        date = datetime.datetime.now()

    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    print(date_obj)

    if not pd.api.types.is_datetime64_dtype(operation['Дата операции']):
        operation['Дата операции'] = pd.to_datetime(operation['Дата операции'], dayfirst=True)
        print(operation['Дата операции'].dtype)

    normalize_category: str = category.strip().capitalize()
    print(normalize_category)

    start_date = date_obj - datetime.timedelta(days=90)
    print(start_date)

    filtered_operation = operation.loc[
        (operation['Дата операции'].notnull()) &
        (operation['Категория'].notnull()) &
        (operation['Категория'] == normalize_category) &
        (operation['Дата операции'] >= start_date) &
        (operation['Дата операции'] <= date_obj)
    ]
    print(filtered_operation.head())

    if len(filtered_operation) != 0:
        grouped_operation = filtered_operation.groupby('Категория')['Сумма операции с округлением'].sum().reset_index()
        return json.dumps(grouped_operation.to_dict(orient='records'))
    else:
        return json.dumps([])
