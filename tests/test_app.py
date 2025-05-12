from unittest.mock import Mock, patch
from src.app import SalaryReporterApp


@patch("src.core.csv_reader.CSVReader.read")
@patch("argparse.ArgumentParser.parse_args")
def test_app_integration(mock_parse, mock_read):
    mock_parse.return_value = Mock(
        files=["test.csv"],
        report="payout"
    )
    mock_read.return_value = [
        {"name": "Test", "department": "Dept", "hours": 40, "rate": 10}
    ]

    app = SalaryReporterApp()
    app.run()  # Проверяем что не возникает исключений
