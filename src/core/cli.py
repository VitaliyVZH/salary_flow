import argparse


class CommandLineParser:
    """Парсер аргументов командной строки"""

    @staticmethod
    def parse(*args) -> argparse.Namespace:
        """Парсинг аргументов"""
        parser = argparse.ArgumentParser(
            description='Генератор отчетов по зарплатам сотрудников'
        )
        parser.add_argument(
            'files', 
            nargs='+',
            help='Пути к CSV файлам с данными'
        )
        parser.add_argument(
            '--report',
            required=True,
            help='Тип отчета (payout/detailed_payout)'
        )
        return parser.parse_args(*args)
