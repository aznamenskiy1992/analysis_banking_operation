import json

import pandas as pd

from src.data import get_data


def filter_transaction_by_search_str(search_str: str) -> str:
    """
    Фильтрует транзакции по строке поиска, проверяя совпадения в полях 'Категория' и 'Описание'.

    Аргументы:
        search_str (str): Строка для поиска в транзакциях. Регистр не учитывается.

    Возвращает:
        str: JSON-строка с отфильтрованными транзакциями, где:
             - search_str найдена в поле 'Категория' (без учета регистра)
             - ИЛИ search_str найдена в поле 'Описание' (без учета регистра)
             Если совпадений нет, возвращается пустой список в формате JSON.

    Исключения:
        ValueError: Если search_str не передана (None)
        TypeError: Если search_str передана не в виде строки
    """
    # Проверка входных параметров
    if search_str is None:
        raise ValueError("Строка для поиска не передана")
    elif not isinstance(search_str, str):
        raise TypeError("Строка передана не в типе str")

    # Приведение строки поиска к нижнему регистру для регистронезависимого поиска
    search_str_lower = search_str.lower()

    # Получение данных транзакций
    operations: pd.DataFrame = get_data()

    # Конвертация DataFrame в список словарей для удобной обработки
    operations_to_list: list[dict] = operations.to_dict(orient="records")

    # Фильтрация и возврат результата в формате JSON:
    # 1. Итерируемся по всем транзакциям
    # 2. Проверяем наличие search_str в полях 'Категория' или 'Описание' (без учета регистра)
    # 3. Сериализуем результат в JSON
    return json.dumps(
        [
            item
            for item in operations_to_list
            if search_str_lower in item["Категория"].lower() or search_str_lower in item["Описание"].lower()
        ]
    )
