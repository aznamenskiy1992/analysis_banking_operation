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

    # Создаём DataFrame с расходами и с переводами и наличными
    cash_and_transfers_categories: list = ['Наличные', 'Переводы']
    expenses: pd.DataFrame = operation.loc[~operation['category'].isin(cash_and_transfers_categories)]
    cash_and_transfers: pd.DataFrame = operation.loc[operation['category'].isin(cash_and_transfers_categories)]

    # Считаем общую сумму расходов
    total_amount: int = round(expenses['amount'].sum())

    # Считаем расходы по категориям
    grouped_expenses: pd.DataFrame = (
        expenses.groupby(['category'])['amount']
        .sum()
        .round()
        .sort_values(ascending=False)
        .reset_index()
    )
    expenses_by_categories: list[dict] = grouped_expenses.iloc[:7].to_dict(orient='records')
    expenses_in_other_category: int = grouped_expenses.iloc[7:]['amount'].sum()
    if expenses_in_other_category > 0:
        expenses_by_categories.append(
            {
                "category": "Остальное",
                "amount": expenses_in_other_category
            }
        )

    # Считаем сумму по переводам и наличным
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
