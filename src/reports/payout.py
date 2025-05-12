from collections import defaultdict
from typing import List, Dict
from .base import BaseReport


class PayoutReport(BaseReport):
    """Отчет с точным позиционированием заголовка Name"""

    NAME_PADDING = 18  # Количество дефисов перед именем
    COLUMN_WIDTHS = (25, 10, 10, 15)  # Ширина после дефисов
    DIVIDER = "-" * NAME_PADDING

    @property
    def name(self) -> str:
        return 'payout'

    def generate(self, data: List[Dict]) -> str:
        self._validate_data(data)

        report = []
        departments = defaultdict(list)

        # Формируем заголовок с учетом отступа
        header = (
            f"{' ' * self.NAME_PADDING}"
            f"{'Name':<{self.COLUMN_WIDTHS[0]}} "
            f"{'Hours':<{self.COLUMN_WIDTHS[1]}} "
            f"{'Rate':<{self.COLUMN_WIDTHS[2]}} "
            f"{'Payout':<{self.COLUMN_WIDTHS[3]}}"
        )
        report.append(header)

        # Группируем данные по отделам
        for emp in data:
            departments[emp['department']].append(emp)

        # Формируем данные
        for dept, employees in departments.items():
            report.append(f"{dept}")

            total_hours = 0.0
            total_payout = 0.0

            # Строки сотрудников
            for emp in employees:
                hours = emp['hours']
                rate = emp['rate']
                payout = hours * rate
                total_hours += hours
                total_payout += payout

                line = (
                    f"{self.DIVIDER}"
                    f"{emp['name']:<{self.COLUMN_WIDTHS[0]}} "
                    f"{hours:<{self.COLUMN_WIDTHS[1]}.1f} "
                    f"{rate:<{self.COLUMN_WIDTHS[2]}.1f} "
                    f"${payout:<{self.COLUMN_WIDTHS[3] - 1},.2f}"
                )
                report.append(line)

            # Итоговая строка
            total_line = (
                f"{' ' * self.NAME_PADDING}"
                f"{' ' * self.COLUMN_WIDTHS[0]} "
                f"{total_hours:<{self.COLUMN_WIDTHS[1]},.0f} "
                f"{'':<{self.COLUMN_WIDTHS[2]}} "
                f"${total_payout:<{self.COLUMN_WIDTHS[3] - 1},.2f}"
            )
            report.append(total_line)

        return '\n'.join(report)
