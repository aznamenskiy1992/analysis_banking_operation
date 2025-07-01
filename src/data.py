import pandas as pd


def get_data() -> pd.DataFrame:
    """Функция возвращает DataFrame с банковскими операциями"""
    try:
        return pd.read_excel('../data/operations.xlsx')
    except FileNotFoundError:
        raise FileNotFoundError('Файл не найден')
