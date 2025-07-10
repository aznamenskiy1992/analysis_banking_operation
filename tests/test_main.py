from unittest.mock import patch

import pandas as pd

from src.main import main


@patch("builtins.input")
@patch("src.main.get_expenses_for_3_months_by_category")
@patch("src.main.filter_transaction_by_search_str")
@patch("src.main.get_events")
@patch("src.main.get_data")
def test_get_main_data_for_main(
    mock_get_data,
    mock_get_events,
    mock_filter_transaction_by_search_str,
    mock_get_expenses_for_3_months_by_category,
    mock_input,
    result_all_functions_for_main,
    capsys,
):
    """Тестирует вывод результата от всех функций программы"""

    mock_get_data.return_value = pd.DataFrame(result_all_functions_for_main["get_data"])
    mock_get_events.return_value = result_all_functions_for_main["get_events"]
    mock_filter_transaction_by_search_str.return_value = result_all_functions_for_main[
        "filter_transaction_by_search_str"
    ]
    mock_get_expenses_for_3_months_by_category.return_value = result_all_functions_for_main[
        "get_expenses_for_3_months_by_category"
    ]

    mock_input.side_effect = ["2025-07-07", "Y", "Супермаркеты", "Супермаркеты", "2025-07-06"]

    main()

    events_result = '{"expenses": {"total_amount": 0,"main": [],"transfers_and_cash": []}}\n'
    filter_result = "[]\n"
    expenses_result = "[]\n"

    captured = capsys.readouterr()
    assert captured.out == events_result + filter_result + expenses_result
