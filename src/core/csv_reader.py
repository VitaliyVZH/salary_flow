# src/core/csv_reader.py
from typing import List, Dict, Set
from pathlib import Path


class CSVReader:
    """Чтение и валидация CSV файлов"""

    RATE_COLUMNS: Set[str] = {'hourly_rate', 'rate', 'salary'}
    REQUIRED_COLUMNS: List[str] = ['department', 'hours_worked', 'name']

    def read(self, file_path: Path) -> List[Dict[str, float]]:
        """Основной метод чтения файла"""
        with open(file_path, 'r') as f:
            headers = self._process_header(f.readline())
            return [
                self._process_line(line, headers, i + 2)
                for i, line in enumerate(f)
                if line.strip()
            ]

    def _process_header(self, header_line: str) -> Dict[str, int]:
        """Обработка строки заголовков"""
        headers = header_line.strip().split(',')
        self._validate_headers(headers)
        return {
            'name': headers.index('name'),
            'department': headers.index('department'),
            'hours': headers.index('hours_worked'),
            'rate': self._find_rate_column(headers)
        }

    def _find_rate_column(self, headers: List[str]) -> int:
        """Поиск колонки со ставкой"""
        for i, h in enumerate(headers):
            if h in self.RATE_COLUMNS:
                return i
        raise ValueError(f"Rate column not found in {headers}")

    def _validate_headers(self, headers: List[str]) -> None:
        """Валидация структуры файла"""
        missing = [c for c in self.REQUIRED_COLUMNS if c not in headers]
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")

    @staticmethod
    def _process_line(
            line: str,
            headers: Dict[str, int],
            line_num: int
    ) -> Dict[str, float]:
        """Парсинг строки данных"""
        parts = line.strip().split(',')
        try:
            return {
                'name': parts[headers['name']].strip(),
                'department': parts[headers['department']].strip(),
                'hours': float(parts[headers['hours']]),
                'rate': float(parts[headers['rate']])
            }
        except (IndexError, ValueError) as e:
            raise ValueError(
                f"Line {line_num}: Invalid data - {str(e)}"
            ) from e
