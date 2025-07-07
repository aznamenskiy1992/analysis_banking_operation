import pandas as pd


def get_expenses(operation: pd.DataFrame) -> dict:
    """
    Функция возвращает:
    1. Общую сумму расходов
    2. Траты по топ-7 категориям
    3. Траты по категориям наличные и переводы
    """
    operation = operation.rename(columns={
        'Категория': 'category',
        'Сумма операции с округлением': 'amount',
    })

    cash_and_transfers_categories: list = ['Переводы', 'Наличные']

    # Находим категории расходов
    expenses_categories: list = operation.loc[
        (operation['Сумма операции'] < 0) &
        (~operation['category'].isin(cash_and_transfers_categories))
    ]['category'].to_list()

    # Создаём DataFrame с расходами и с переводами и наличными
    expenses: pd.DataFrame = operation.loc[operation['category'].isin(expenses_categories)]
    cash_and_transfers: pd.DataFrame = operation.loc[operation['category'].isin(cash_and_transfers_categories)]

    # Считаем общую сумму расходов
    total_amount: int = round(expenses['amount'].sum()) + round(cash_and_transfers['amount'].sum())

    # Считаем расходы по категориям
    if len(expenses) == 0:
        expenses_by_categories: list = []
    else:
        grouped_expenses: pd.DataFrame = (
            expenses.groupby(['category'])['amount']
            .sum()
            .round()
            .sort_values(ascending=False)
            .reset_index()
        )
        expenses_by_categories: list[dict] = grouped_expenses.iloc[:7].to_dict(orient='records')
        if len(expenses_by_categories) == 7:
            expenses_in_other_category: int = grouped_expenses.iloc[7:]['amount'].sum()
            if expenses_in_other_category > 0:
                expenses_by_categories.append(
                    {
                        "category": "Остальное",
                        "amount": expenses_in_other_category
                    }
                )

    # Считаем сумму по переводам и наличным
    if len(cash_and_transfers) == 0:
        result_cash_and_transfers: list = []
    else:
        grouped_cash_and_transfers: pd.DataFrame = (
            cash_and_transfers.groupby(['category'])['amount']
            .sum()
            .round()
            .sort_values(ascending=False)
            .reset_index()
        )
        result_cash_and_transfers: list[dict] = grouped_cash_and_transfers.to_dict(orient='records')

    return {
        "expenses": {
            "total_amount": total_amount,
            "main": expenses_by_categories,
            "transfers_and_cash": result_cash_and_transfers
        }
    }


def get_income(operation: pd.DataFrame) -> dict:
    """Функция возвращает поступления"""
    operation = operation.rename(columns={
        'Описание': 'category',
        'Сумма операции с округлением': 'amount',
    })

    # Создаём DataFrame с поступлениями
    income: pd.DataFrame = operation.loc[operation['Категория'] == 'Пополнения']

    # Считаем общую сумму поступлений
    total_amount: int = round(income['amount'].sum())

    # Считаем поступления по категориям
    if len(income) == 0:
        income_by_categories: list = []
    else:
        grouped_income: pd.DataFrame = (
            income.groupby(['category'])['amount']
            .sum()
            .round()
            .sort_values(ascending=False)
            .reset_index()
        )
        income_by_categories: list[dict] = grouped_income.to_dict(orient='records')

    return {
        "income": {
            "total_amount": total_amount,
            "main": income_by_categories,
        }
    }


def get_currency_rates(currency: list) -> dict:
    """Функция возвращает курс валют из user_settings.json"""
    pass
