from unittest.mock import patch

import pytest

from src.data import get_data


@patch("pandas.read_excel")
def test_file_not_found_for_get_data(mock_read_excel):
    """Тестирует кейс, когда файл не найден"""
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")

    with pytest.raises(FileNotFoundError) as exc_info:
        get_data()
    assert str(exc_info.value) == "Файл не найден"
