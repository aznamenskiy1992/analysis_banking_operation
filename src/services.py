import json
import logging

import pandas as pd

from src.data import get_data


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def filter_transaction_by_search_str(operation: list[dict], search_str: str) -> str:
    """
    Фильтрует транзакции по строке поиска, проверяя совпадения в полях 'Категория' и 'Описание'.

    Аргументы:
        search_str (str): Строка для поиска в транзакциях. Регистр не учитывается.

    Возвращает:
        operation: список словарей с транзакциями
        str: JSON-строка с отфильтрованными транзакциями, где:
             - search_str найдена в поле 'Категория' (без учета регистра)
             - ИЛИ search_str найдена в поле 'Описание' (без учета регистра)
             Если совпадений нет, возвращается пустой список в формате JSON.

    Исключения:
        ValueError: Если search_str не передана (None)
        TypeError: Если search_str передана не в виде строки
    """
    # Проверка входных параметров
    if operation is None:
        logger.critical('Ошибка: Не переданы транзакции')
        raise ValueError("Транзакции не переданы")
    elif not isinstance(operation, list):
        logger.critical(f'Ошибка: Транзакции переданы в типе {type(operation)}')
        raise TypeError("Транзакции должны быть переданы в списке")

    if search_str is None:
        logger.critical('Ошибка: Не передана строка для поиска')
        raise ValueError("Строка для поиска не передана")
    elif not isinstance(search_str, str):
        logger.critical(f'Ошибка: Строка для поиска передана в типе {type(search_str)}')
        raise TypeError("Строка передана не в типе str")

    # Приведение строки поиска к нижнему регистру для регистронезависимого поиска
    search_str_lower = search_str.lower()

    # Фильтрация и возврат результата в формате JSON:
    # 1. Итерируемся по всем транзакциям
    # 2. Проверяем наличие search_str в полях 'Категория' или 'Описание' (без учета регистра)
    # 3. Сериализуем результат в JSON
    return json.dumps(
        [
            item
            for item in operation
            if search_str_lower in item["Категория"].lower() or search_str_lower in item["Описание"].lower()
        ]
    )
