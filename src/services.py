import pandas as pd
import json
from src.data import get_data


def filter_transaction_by_search_str(search_str: str) -> json:
    """Функция фильтрует DataFrame с операцими по строке"""
    if search_str is None:
        raise ValueError('Строка для поиска не передана')

    search_str_lower = search_str.lower()

    operations: pd.DataFrame = get_data()
    operations_to_list: list[dict] = operations.to_dict(orient='records')

    return json.dumps([item for item in operations_to_list if search_str_lower in item['Категория'].lower() or search_str_lower in item['Описание'].lower()])
