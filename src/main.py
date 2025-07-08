import pandas as pd

from src.data import get_data
from src.reports import get_expenses_for_3_months_by_category
from src.services import filter_transaction_by_search_str
from src.views import get_events


def main() -> None:
    """Функция выводит результат работы всех функций программы"""
    operations: pd.DataFrame = get_data()

    get_events_date_arg = input("Введите дату до которой собрать данные. Маска: YYYY-MM-DD")
    get_events_period_arg = input(
        """Укажите за какой период собрать данные.
    Возможные значения:
    W - неделя, на которую приходится дата
    Y -  год, на который приходится дата
    ALL - все данные до указанной даты"""
    )
    print(get_events(operations, get_events_date_arg, get_events_period_arg))

    filter_transaction_search_str_arg = input("Укажите категорию по которой отфильтровать транзакции")
    print(filter_transaction_by_search_str(operations.to_dict(orient="records"), filter_transaction_search_str_arg))

    get_expenses_category_arg = input("Укажите категорию по которой будет сформирован отчёт")
    get_expenses_date_arg = input(
        """Вы можете указать дату за которую будет сформирован отчёт. Маска: YYYY-MM-DD
    Если дата не указана, отчёт сформируется за сегодня"""
    )
    print(get_expenses_for_3_months_by_category(operations, get_expenses_category_arg, get_expenses_date_arg))

    return None
