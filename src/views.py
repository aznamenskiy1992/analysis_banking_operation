from typing import Optional
import json

import pandas as pd

from src.utils import get_expenses, get_income, get_currency_rates, get_stock_prices


def get_events(operation: pd.DataFrame, date_: str, period: Optional[str] = 'M') -> str:
    """Функция возвращает события"""
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
