import pytest
from unittest.mock import patch

from src.data import get_data


def test_file_not_found_for_get_data():
    """Тестирует кейс, когда файл не найден"""
    with pytest.raises(FileNotFoundError) as exc_info:
        get_data()

    assert str(exc_info.value) == 'Файл не найден'
