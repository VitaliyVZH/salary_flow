from pathlib import Path
import pytest
from src.core.csv_reader import CSVReader


def test_valid_csv_reading(tmp_path):
    csv_content = """name,department,hours_worked,rate
John Doe,Engineering,160,50
Jane Smith,Marketing,150,55"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)

    reader = CSVReader()
    data = reader.read(file_path)

    assert len(data) == 2
    assert data[0]["name"] == "John Doe"
    assert data[1]["rate"] == 55.0


def test_missing_column(tmp_path):
    # Создаем временный файл с некорректными заголовками
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("name,hours_worked,rate\nJohn Doe,160,50")  # Нет колонки department

    reader = CSVReader()

    with pytest.raises(ValueError) as exc:
        reader.read(file_path)

    assert "Missing columns: department" in str(exc.value)
