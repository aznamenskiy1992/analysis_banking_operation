import pandas as pd


def get_data() -> pd.DataFrame:
    """
    Загружает банковские операции из Excel-файла в DataFrame.

    Возвращает:
        pd.DataFrame: DataFrame с банковскими операциями, загруженными из файла.
                      Структура колонок зависит от содержимого файла operations.xlsx.

    Исключения:
        FileNotFoundError: Если файл operations.xlsx не найден по указанному пути.

    Особенности:
        - Ожидает, что файл находится в директории ../data/ относительно текущей
        - Файл должен быть в формате Excel (.xlsx)
    """
    try:
        # Пытаемся загрузить данные из Excel-файла
        # Путь к файлу: ../data/operations.xlsx (на уровень выше в папке data)
        return pd.read_excel("../data/operations.xlsx")

    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        raise FileNotFoundError("Файл не найден")
