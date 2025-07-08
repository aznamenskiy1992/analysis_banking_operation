import datetime
import json
import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def get_expenses_for_3_months_by_category(operation: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по указанной категории за последние 3 месяца в формате JSON.

    Принимает:
        operation (pd.DataFrame): DataFrame с транзакциями, должен содержать колонки:
                                 'Дата операции', 'Категория', 'Сумма операции с округлением'
        category (str): Название категории для фильтрации транзакций
        date (Optional[str], optional): Дата в формате YYYY-MM-DD. Если не указана,
                                      используется текущая дата. Defaults to None.

    Возвращает:
        str: JSON-строка с результатами агрегации или пустой список, если транзакции не найдены

    Исключения:
        ValueError: Если не переданы транзакции или категория, или если дата в неверном формате
        TypeError: Если переданы аргументы неверного типа
    """
    # Валидация входных данных: проверка наличия и типа транзакций
    if operation is None:
        logger.critical("Ошибка: Не переданы транзакции")
        raise ValueError("Транзакции не переданы")
    elif not isinstance(operation, pd.DataFrame):
        logger.critical(f"Ошибка: Транзакции переданы в типе {type(operation)}")
        raise TypeError("Транзакции должны быть переданы в виде pandas DataFrame")

    # Валидация категории: проверка наличия и типа
    if category is None:
        logger.critical("Ошибка: Категория не передана")
        raise ValueError("Категория не передана")
    elif not isinstance(category, str):
        logger.critical(f"Ошибка: Категория передана в типе {type(category)}")
        raise TypeError("Категория должна быть передана в виде str")

    # Обработка даты: если не указана - берем текущую, иначе парсим строку
    if date is None:
        date_obj = datetime.datetime.now()
    else:
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except ValueError:
            logger.critical(f"Ошибка: Дата ({date, type(date)}) не конвертируется в datetime")
            raise ValueError("Дата указана неверно. Маска: YYYY-MM-DD")

    # Конвертируем колонку с датами в datetime, если это еще не сделано
    if not pd.api.types.is_datetime64_dtype(operation["Дата операции"]):
        operation["Дата операции"] = pd.to_datetime(operation["Дата операции"], dayfirst=True)

    # Нормализуем категорию (удаляем пробелы и приводим к стандартному виду)
    normalize_category: str = category.strip().capitalize()

    # Вычисляем дату начала периода (90 дней назад от указанной даты)
    start_date = date_obj - datetime.timedelta(days=90)

    # Фильтруем транзакции по:
    # - наличию даты и категории
    # - соответствию указанной категории
    # - попаданию в временной диапазон (последние 3 месяца)
    filtered_operation = operation.loc[
        (operation["Дата операции"].notnull())
        & (operation["Категория"].notnull())
        & (operation["Категория"] == normalize_category)
        & (operation["Дата операции"] >= start_date)
        & (operation["Дата операции"] <= date_obj)
    ]

    # Если найдены подходящие транзакции - группируем по категории и суммируем суммы
    if len(filtered_operation) != 0:
        grouped_operation = filtered_operation.groupby("Категория")["Сумма операции с округлением"].sum().reset_index()
        return json.dumps(grouped_operation.to_dict(orient="records"))
    else:
        # Если транзакций не найдено - возвращаем пустой список в JSON
        return json.dumps([])
