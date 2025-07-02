from typing import Optional

import pandas as pd
import datetime


def get_expenses_for_3_months_by_category(operation: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по категории за последние 3 месяца"""
