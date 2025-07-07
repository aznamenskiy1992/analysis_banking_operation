import datetime
from typing import Optional
import json

import pandas as pd

from src.utils import get_expenses, get_income, get_currency_rates, get_stock_prices


def get_events(operation: pd.DataFrame, date_: str, period: Optional[str] = 'M') -> str:
    """Функция возвращает события"""
    if date_ is None:
        raise ValueError('Дата не передана')

    try:
        date_obj = datetime.datetime.strptime(date_, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    except ValueError:
        raise ValueError('Дата указана неверно. Маска: YYYY-MM-DD')

    if not pd.api.types.is_datetime64_dtype(operation['Дата операции']):
        operation['Дата операции'] = pd.to_datetime(operation['Дата операции'], dayfirst=True)

    if period != 'ALL':
        if period == 'W':
            start_date = (date_obj - datetime.timedelta(days=date_obj.weekday())).replace(hour=00, minute=00, second=00)
        elif period == 'M':
            start_date = date_obj.replace(day=1, hour=00, minute=00, second=00)
        elif period == 'Y':
            start_date = date_obj.replace(month=1, day=1, hour=00, minute=00, second=00)
        operation = operation.loc[
            (operation['Дата операции'] >= start_date) &
            (operation['Дата операции'] <= date_obj)
        ]
    else:
        operation = operation.loc[operation['Дата операции'] <= date_obj]

    with open('user_settings.json') as f:
        currencies_and_stocks: dict = json.load(f)

    currencies: list = currencies_and_stocks.get("user_currencies", [])
    stocks: list = currencies_and_stocks.get("user_stocks", [])

    expenses: dict = json.loads(get_expenses(operation))
    income: dict = json.loads(get_income(operation))
    currency_rates: dict = json.loads(get_currency_rates(currencies))
    stock_rates: dict = json.loads(get_stock_prices(stocks))

    merged_events_data: dict = {**expenses, **income, **currency_rates, **stock_rates}

    return json.dumps(merged_events_data)
