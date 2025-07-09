import datetime
import json
import logging
from typing import Optional

import pandas as pd

from src.utils import get_currency_rates, get_expenses, get_income, get_stock_prices

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def get_events(operation: pd.DataFrame, date_: str, period: Optional[str] = "M") -> str:
    """Функция возвращает агрегированные финансовые события за указанный период в формате JSON.

    Собирает данные о:
    - Расходах
    - Доходах
    - Курсах валют
    - Ценах акций
    и объединяет их в единый JSON-объект.

    Принимает:
        operation (pd.DataFrame): DataFrame с транзакциями, должен содержать колонку 'Дата операции'
        date_ (str): Конечная дата периода в формате YYYY-MM-DD
        period (Optional[str], optional): Период для выборки данных. Варианты:
            "W" - неделя (на которой находится date_)
            "M" - месяц (по умолчанию)
            "Y" - год
            "ALL" - все данные до date_

    Возвращает:
        str: JSON-строка с объединенными данными о событиях

    Исключение:
        ValueError: Если дата не передана или имеет неверный формат
    """
    # Проверка наличия даты
    if date_ is None:
        logger.critical("Дата не передана")
        raise ValueError("Дата не передана")

    # Парсинг даты с проверкой формата
    try:
        date_obj = datetime.datetime.strptime(date_, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    except ValueError:
        logger.critical(f"Ошибка: Дата ({date_, type(date_)}) не конвертируется в datetime")
        raise ValueError("Дата указана неверно. Маска: YYYY-MM-DD")

    # Конвертация колонки с датами в datetime, если необходимо
    if not pd.api.types.is_datetime64_dtype(operation["Дата операции"]):
        operation["Дата операции"] = pd.to_datetime(operation["Дата операции"], dayfirst=True)

    # Фильтрация данных по периоду
    if period != "ALL":
        # Определение начальной даты в зависимости от периода
        if period == "W":
            # Для недели - начало недели (понедельник)
            start_date = (date_obj - datetime.timedelta(days=date_obj.weekday())).replace(
                hour=00, minute=00, second=00
            )
        elif period == "M":
            # Для месяца - первое число месяца
            start_date = date_obj.replace(day=1, hour=00, minute=00, second=00)
        elif period == "Y":
            # Для года - первое число года
            start_date = date_obj.replace(month=1, day=1, hour=00, minute=00, second=00)

        # Фильтрация операций по временному диапазону
        operation = operation.loc[
            (operation["Дата операции"] >= start_date) & (operation["Дата операции"] <= date_obj)
        ]
    else:
        # Для ALL - все операции до указанной даты
        operation = operation.loc[operation["Дата операции"] <= date_obj]

    # Загрузка пользовательских настроек по валютам и акциям
    with open("../user_settings.json") as f:
        currencies_and_stocks: dict = json.load(f)

    # Получение списка валют и акций из настроек
    currencies: list = currencies_and_stocks.get("user_currencies", [])
    stocks: list = currencies_and_stocks.get("user_stocks", [])

    # Сбор данных из различных источников
    expenses: dict = json.loads(get_expenses(operation))  # Получение расходов
    income: dict = json.loads(get_income(operation))  # Получение доходов
    currency_rates: dict = json.loads(get_currency_rates(currencies))  # Получение курсов валют
    stock_rates: dict = json.loads(get_stock_prices(stocks))  # Получение цен акций

    # Объединение всех данных в один словарь
    merged_events_data: dict = {**expenses, **income, **currency_rates, **stock_rates}

    # Возврат объединенных данных в формате JSON
    return json.dumps(merged_events_data)
