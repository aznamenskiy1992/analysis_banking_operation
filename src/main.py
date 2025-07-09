import pandas as pd

from src.data import get_data
from src.reports import get_expenses_for_3_months_by_category
from src.services import filter_transaction_by_search_str
from src.views import get_events


def main() -> None:
    """Основная функция программы, которая выполняет последовательность операций:
    1. Получает данные о транзакциях
    2. Запрашивает у пользователя параметры для выборки данных
    3. Выводит результаты работы всех функций программы

    Функция не принимает аргументов и не возвращает значений (None)
    """
    # Получаем DataFrame с операциями из функции get_data()
    operations: pd.DataFrame = get_data()

    # Запрашиваем у пользователя дату для выборки данных
    get_events_date_arg = input("Введите дату до которой собрать данные. Маска: YYYY-MM-DD")
    # Запрашиваем период для выборки данных (неделя, год или все данные)
    get_events_period_arg = input(
        """Укажите за какой период собрать данные.
    Возможные значения:
    W - неделя, на которую приходится дата
    Y -  год, на который приходится дата
    ALL - все данные до указанной даты"""
    )
    # Выводим результат функции get_events с пользовательскими параметрами
    print(get_events(operations, get_events_date_arg, get_events_period_arg))

    # Запрашиваем категорию для фильтрации транзакций
    filter_transaction_search_str_arg = input("Укажите категорию по которой отфильтровать транзакции")
    # Преобразуем DataFrame в список словарей и фильтруем по категории
    print(filter_transaction_by_search_str(operations.to_dict(orient="records"), filter_transaction_search_str_arg))

    # Запрашиваем категорию для формирования отчета по расходам
    get_expenses_category_arg = input("Укажите категорию по которой будет сформирован отчёт")
    # Запрашиваем дату для отчета (если не указана - будет использована текущая дата)
    get_expenses_date_arg = input(
        """Вы можете указать дату за которую будет сформирован отчёт. Маска: YYYY-MM-DD
    Если дата не указана, отчёт сформируется за сегодня"""
    )
    # Выводим отчет по расходам за 3 месяца для указанной категории
    print(get_expenses_for_3_months_by_category(operations, get_expenses_category_arg, get_expenses_date_arg))

    return None


if __name__ == "__main__":
    main()
