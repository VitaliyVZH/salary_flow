import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.core.cli import CommandLineParser
from src.core.csv_reader import CSVReader
from src.reports.payout import PayoutReport


# Фикстуры для тестовых данных
@pytest.fixture
def sample_csv_data():
    return [
        "name,department,hours_worked,rate\n",
        "Alice Johnson,Marketing,160,50\n",
        "Bob Smith,Design,150,40\n"
    ]


@pytest.fixture
def broken_csv_data():
    return [
        "department,hours_worked\n",
        "Marketing,160\n"
    ]


# Тесты для CSVReader
class TestCSVReader:
    def test_read_valid_file(self, sample_csv_data):
        reader = CSVReader()
        with patch('builtins.open', mock_open(read_data=''.join(sample_csv_data))):
            data = reader.read(Path("dummy.csv"))
            assert len(data) == 2
            assert data[0]["name"] == "Alice Johnson"
            assert data[1]["rate"] == 40.0

    def test_missing_columns(self, broken_csv_data):
        reader = CSVReader()
        with patch('builtins.open', mock_open(read_data=''.join(broken_csv_data))), \
                pytest.raises(ValueError):
            reader.read(Path("invalid.csv"))


# Тесты для PayoutReport
class TestPayoutReport:
    @pytest.fixture
    def test_data(self):
        return [
            {"name": "Alice Johnson", "department": "IT", "hours": 160, "rate": 45},
            {"name": "Bob Smith", "department": "IT", "hours": 150, "rate": 50}
        ]

    def test_report_generation(self, test_data):
        report = PayoutReport()
        result = report.generate(test_data)

        # Проверяем, что в результате есть название отдела и общая сумма
        assert "IT" in result
        assert "$14,700.00" in result


class TestPayoutReport:
    @pytest.fixture
    def test_data(self):
        return [
            {"name": "Alice Johnson", "department": "IT", "hours": 160, "rate": 45},
            {"name": "Bob Smith", "department": "IT", "hours": 150, "rate": 50}
        ]

    def test_report_generation(self, test_data):
        report = PayoutReport()
        result = report.generate(test_data)

        # Проверяем, что в результате есть название отдела и общая сумма
        assert "IT" in result
        assert "$14,700.00" in result


# Интеграционные тесты
class TestIntegration:
    def test_full_flow(self, sample_csv_data):
        with patch('builtins.open', mock_open(read_data=''.join(sample_csv_data))):
            parser = CommandLineParser()
            args = parser.parse(["dummy.csv", "--report", "payout"])

            reader = CSVReader()
            data = reader.read(Path("dummy.csv"))

            report = PayoutReport()
            output = report.generate(data)

            assert "Marketing" in output
            assert "Design" in output

    def test_error_handling(self):
        with pytest.raises(SystemExit):
            parser = CommandLineParser()
            parser.parse(["--report", "payout"])  # Не указаны файлы
