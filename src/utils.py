import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


load_dotenv()
currency_data_api_key = os.getenv("CURRENCY_DATA_API_KEY")
marketstack_api_key = os.getenv("MARKETSTACK_API_KEY")


def get_expenses(operation: pd.DataFrame) -> str:
    """
    Анализирует расходы из DataFrame операций и возвращает структурированные данные в формате JSON.

    Возвращает:
    1. Общую сумму всех расходов (включая наличные и переводы)
    2. Топ-7 категорий расходов (по сумме)
    3. Отдельно расходы по категориям 'Наличные' и 'Переводы'

    Принимает:
        operation (pd.DataFrame): DataFrame с операциями, должен содержать колонки:
                                'Категория', 'Сумма операции', 'Сумма операции с округлением'

    Возвращает:
        str: JSON-строка с структурированными данными о расходах, включая:
            - total_amount: общая сумма расходов
            - main: топ-7 категорий расходов
            - transfers_and_cash: расходы по наличным и переводам

    Особенности:
        - Отрицательные значения суммы считаются расходами
        - Категории 'Наличные' и 'Переводы' обрабатываются отдельно
        - Если категорий больше 7, остальные объединяются в категорию 'Остальное'
    """
    # Переименовываем колонки для удобства работы
    operation = operation.rename(
        columns={
            "Категория": "category",
            "Сумма операции с округлением": "amount",
        }
    )

    # Категории, которые нужно обработать отдельно
    cash_and_transfers_categories: list = ["Переводы", "Наличные"]

    # Находим все категории расходов (отрицательные суммы, исключая наличные и переводы)
    expenses_categories: list = operation.loc[
        (operation["Сумма операции"] < 0) & (~operation["category"].isin(cash_and_transfers_categories))
    ]["category"].to_list()

    # Создаем отдельные DataFrame:
    # - expenses: обычные расходы по категориям
    # - cash_and_transfers: только наличные и переводы
    expenses: pd.DataFrame = operation.loc[operation["category"].isin(expenses_categories)]
    cash_and_transfers: pd.DataFrame = operation.loc[operation["category"].isin(cash_and_transfers_categories)]

    # Суммируем общие расходы (обычные + наличные/переводы)
    total_amount: int = round(expenses["amount"].sum()) + round(cash_and_transfers["amount"].sum())

    # Анализ расходов по категориям (топ-7)
    if len(expenses) == 0:
        logger.info("Расходы по категориям не найдены")
        expenses_by_categories: list = []
    else:
        # Группируем по категориям, суммируем и сортируем по убыванию
        grouped_expenses: pd.DataFrame = (
            expenses.groupby(["category"])["amount"].sum().round().sort_values(ascending=False).reset_index()
        )
        # Берем топ-7 категорий
        expenses_by_categories: list[dict] = grouped_expenses.iloc[:7].to_dict(orient="records")
        # Если есть еще категории - объединяем в 'Остальное'
        if len(expenses_by_categories) == 7:
            expenses_in_other_category: int = grouped_expenses.iloc[7:]["amount"].sum()
            if expenses_in_other_category > 0:
                expenses_by_categories.append({"category": "Остальное", "amount": expenses_in_other_category})

    # Анализ расходов по наличным и переводам
    if len(cash_and_transfers) == 0:
        logger.info("Переводы и наличные не найдены")
        result_cash_and_transfers: list = []
    else:
        # Группируем и сортируем наличные/переводы
        grouped_cash_and_transfers: pd.DataFrame = (
            cash_and_transfers.groupby(["category"])["amount"].sum().round().sort_values(ascending=False).reset_index()
        )
        result_cash_and_transfers: list[dict] = grouped_cash_and_transfers.to_dict(orient="records")

    # Формируем итоговый JSON с красивым форматированием
    return json.dumps(
        {
            "expenses": {
                "total_amount": total_amount,  # Общая сумма расходов
                "main": expenses_by_categories,  # Топ-7 категорий
                "transfers_and_cash": result_cash_and_transfers,  # Наличные и переводы
            }
        }, ensure_ascii=False, indent=4
    )


def get_income(operation: pd.DataFrame) -> str:
    """
    Анализирует поступления (доходы) из DataFrame операций и возвращает структурированные данные в формате JSON.

    Функция обрабатывает операции с категорией "Пополнения" и возвращает:
    1. Общую сумму всех поступлений
    2. Детализацию поступлений по категориям (из поля "Описание")

    Принимает:
        operation (pd.DataFrame): DataFrame с операциями, должен содержать колонки:
                               'Категория', 'Описание', 'Сумма операции с округлением'

    Возвращает:
        str: JSON-строка с данными о поступлениях в формате:
            {
                "income": {
                    "total_amount": общая сумма поступлений,
                    "main": список категорий поступлений с суммами
                }
            }

    Особенности:
        - Использует поле 'Описание' как категорию для классификации поступлений
        - Все суммы округляются до целых чисел
        - Возвращает JSON с отступами для удобного чтения
    """
    # Переименование колонок для удобства обработки
    operation = operation.rename(
        columns={
            "Описание": "category",  # Используем поле 'Описание' как категорию поступлений
            "Сумма операции с округлением": "amount",  # Сумма операции
        }
    )

    # Фильтруем только операции пополнения (доходы)
    income: pd.DataFrame = operation.loc[operation["Категория"] == "Пополнения"]

    # Считаем общую сумму всех поступлений с округлением
    total_amount: int = round(income["amount"].sum())

    # Анализ поступлений по категориям (из поля Описание)
    if len(income) == 0:
        logger.info("Поступления по категориям не найдены")
        income_by_categories: list = []
    else:
        # Группируем по категориям, суммируем суммы, сортируем по убыванию
        grouped_income: pd.DataFrame = (
            income.groupby(["category"])["amount"].sum().round().sort_values(ascending=False).reset_index()
        )
        # Конвертируем в список словарей
        income_by_categories: list[dict] = grouped_income.to_dict(orient="records")

    # Формируем итоговый JSON с отступами
    return json.dumps(
        {
            "income": {
                "total_amount": total_amount,  # Общая сумма доходов
                "main": income_by_categories,  # Детализация по категориям
            }
        }, ensure_ascii=False, indent=4
    )


def get_currency_rates(currencies: list) -> str:
    """
    Получает текущие курсы валют относительно RUB (российского рубля) через внешний API.

    Функция делает запрос к API курсов валют и возвращает актуальные курсы для указанных валют.
    Обрабатывает ошибки запросов и валидирует входные данные.

    Принимает:
        currencies (list): Список валютных кодов (например, ["USD", "EUR"]), для которых нужно получить курс

    Возвращает:
        str: JSON-строка с курсами валют в формате:
            {
                "currency_rates": [
                    {
                        "currency": "USD",
                        "rate": 75.50
                    },
                    ...
                ]
            }

    Исключения:
        ValueError: Если передан пустой список валют или None
        TypeError: Если валюты переданы не в виде списка
        requests.HTTPError: При ошибках HTTP-запроса к API
        requests.exceptions.RequestException: При других ошибках сетевого запроса

    Особенности:
        - Использует API apilayer.com для получения курсов валют
        - Запрашивает курс на текущую дату
        - Возвращает курс относительно RUB (российского рубля)
        - Форматирует вывод с отступами для удобного чтения
    """
    # Валидация входных данных
    if currencies is None:
        logger.critical("Ошибка: Валюта не передана")
        raise ValueError("Валюты не переданы")
    elif isinstance(currencies, list):
        if len(currencies) == 0:
            logger.critical("Ошибка: Передан пустой список валют")
            raise ValueError("Список валют пустой")
    elif not isinstance(currencies, list):
        logger.critical(f"Ошибка: Валюты переданы в типе {type(currencies)}")
        raise TypeError("Валюты переданы не в списке")

    # Инициализация списка для хранения результатов
    currency_rates: list = []

    # Получение текущей даты в нужном формате
    current_day = datetime.datetime.now()
    current_day_string = current_day.strftime("%Y-%m-%d")

    # Запрос курса для каждой валюты из списка
    for currency in currencies:
        # Формирование URL для API запроса
        domain = "https://api.apilayer.com/currency_data/change?"
        url = f"{domain}start_date={current_day_string}&end_date={current_day_string}&currencies=RUB&source={currency}"

        # Подготовка данных для запроса
        payload = {}
        headers = {"apikey": currency_data_api_key}  # API ключ должен быть определен где-то в коде

        try:
            # Выполнение HTTP GET запроса
            response = requests.get(url, headers=headers, data=payload)
            response.raise_for_status()  # Проверка на ошибки HTTP
            content = response.json()  # Парсинг JSON ответа

        except requests.HTTPError as e:
            # Обработка ошибок HTTP (404, 500 и т.д.)
            logger.critical("Ошибка: HTTPError")
            raise requests.HTTPError(
                f"""Ошибка HTTP: {e}
Причина: {response.reason}"""
            )

        except requests.exceptions.RequestException as e:
            # Обработка других сетевых ошибок
            logger.critical("Ошибка: Другие ошибки при get запросе")
            raise requests.exceptions.RequestException(f"Ошибка: {e}")

        else:
            # Если запрос успешен, извлекаем курс из ответа
            currency_rates.append(
                {
                    "currency": currency,  # Код валюты (например, USD)
                    "rate": content.get("quotes", {}).get(f"{currency}RUB", {}).get("end_rate", 0.00),  # Курс к рублю
                }
            )

    # Возвращаем результат в виде форматированного JSON
    return json.dumps({"currency_rates": currency_rates}, ensure_ascii=False, indent=4)


def get_stock_prices(stocks: list) -> str:
    """
    Получает текущие цены акций через API Marketstack.

    Функция запрашивает цены закрытия для указанных акций за последний торговый день
    и возвращает их в формате JSON.

    Принимает:
        stocks (list): Список тикеров акций (например, ['AAPL', 'MSFT'])

    Возвращает:
        str: JSON-строка с ценами акций в формате:
            {
                "stock_prices": [
                    {
                        "stock": "AAPL",
                        "price": 150.50
                    },
                    ...
                ]
            }

    Исключения:
        ValueError: Если передан пустой список акций или None, либо если в ответе API нет ключа 'data'
        TypeError: Если акции переданы не в виде списка
        requests.HTTPError: При ошибках HTTP-запроса к API
        requests.exceptions.RequestException: При других ошибках сетевого запроса

    Особенности:
        - Использует API marketstack.com для получения данных
        - Запрашивает цены закрытия за последний торговый день (с запасом в 4 дня)
        - Возвращает данные с отступами для удобного чтения
        - Логирует критические ошибки
    """
    # Валидация входных параметров
    if stocks is None:
        logger.critical("Ошибка: Акции не переданы")
        raise ValueError("Акции не переданы")
    elif isinstance(stocks, list):
        if len(stocks) == 0:
            logger.critical("Ошибка: Передан пустой список акций")
            raise ValueError("Список акций пустой")
    elif not isinstance(stocks, list):
        logger.critical(f"Ошибка: Акции переданы в типе {type(stocks)}")
        raise TypeError("Акции переданы не в списке")

    # Инициализация списка для хранения результатов
    stock_prices: list = []

    # Определение даты для запроса (4 дня назад как запасной вариант)
    day_ = datetime.datetime.now() - datetime.timedelta(days=4)
    day_string = day_.strftime("%Y-%m-%d")

    # Базовый URL API
    url = f"https://api.marketstack.com/v1/eod?access_key={marketstack_api_key}"

    # Параметры запроса
    querystring = {
        "symbols": ",".join(stocks),  # Объединяем тикеры через запятую
        "date_from": day_string,  # Начальная дата периода
        "date_to": day_string,  # Конечная дата периода (та же дата)
    }

    try:
        # Выполнение GET-запроса с параметрами
        response = requests.get(url, params=querystring)
        response.raise_for_status()  # Проверка на ошибки HTTP
        content = response.json()  # Парсинг JSON-ответа

    except requests.HTTPError as e:
        # Обработка HTTP-ошибок (404, 500 и т.д.)
        logger.critical("Ошибка: HTTPError")
        raise requests.HTTPError(
            f"""Ошибка HTTP: {e}
        Причина: {response.reason}"""
        )

    except requests.exceptions.RequestException as e:
        # Обработка других сетевых ошибок
        logger.critical("Ошибка: Другие ошибки при get запросе")
        raise requests.exceptions.RequestException(f"Ошибка: {e}")

    else:
        # Проверка наличия ключа 'data' в ответе
        if "data" not in content:
            logger.critical('Ошибка: В ответе нет ключа "data"')
            raise ValueError("В ответе нет ключа data. Проверьте ответ от API")

        # Формирование списка цен акций из ответа API
        stock_prices.extend(
            [
                {
                    "stock": content["data"][i]["symbol"],  # Тикер акции
                    "price": content["data"][i]["close"],  # Цена закрытия
                }
                for i in range(len(content["data"]))
                if "symbol" in content["data"][i] and "close" in content["data"][i]  # Проверка наличия ключей
            ]
        )

    # Возврат результатов в виде форматированного JSON
    return json.dumps({"stock_prices": stock_prices}, ensure_ascii=False, indent=4)
