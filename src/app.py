from typing import List, Type, Dict
from pathlib import Path
from .core.cli import CommandLineParser
from .core.csv_reader import CSVReader
from .reports.base import BaseReport
from .reports.payout import PayoutReport


class ReportManager:
    """Менеджер зарегистрированных отчетов"""

    def __init__(self, reports: List[Type[BaseReport]]):
        self.reports = {cls().name: cls() for cls in reports}

    def get_report(self, name: str) -> BaseReport:
        """Получение обработчика отчета"""
        if name not in self.reports:
            available = ", ".join(self.reports.keys())
            raise ValueError(f"Доступные отчеты: {available}")
        return self.reports[name]


class SalaryReporterApp:
    """Основной класс приложения"""

    def __init__(self):
        self.parser = CommandLineParser()
        self.reader = CSVReader()
        self.report_manager = ReportManager([
            PayoutReport,
        ])

    def run(self) -> None:
        """Запуск основного цикла"""
        try:
            args = self.parser.parse()
            data = self._load_data(args.files)
            report = self.report_manager.get_report(args.report)
            print("\n" + report.generate(data) + "\n")
        except Exception as e:
            self._handle_error(e)

    def _load_data(self, files: List[str]) -> List[Dict]:
        """Загрузка данных из файлов"""
        data = []
        for path in files:
            data.extend(self.reader.read(Path(path)))
        if not data:
            raise ValueError("No valid data found")
        return data

    @staticmethod
    def _handle_error(error: Exception) -> None:
        """Обработка ошибок"""
        error_messages = {
            FileNotFoundError: "Файл не найден: {err}",
            ValueError: "Ошибка данных: {err}",
        }

        msg = next(
            (fmt.format(err=str(error))
             for t, fmt in error_messages.items()
             if isinstance(error, t)
             ), "Неожиданная ошибка: {err}".format(err=str(error)))

        print(f"\nОшибка: {msg}")
        exit(1)
