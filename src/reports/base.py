from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReport(ABC):
    """Абстрактный базовый класс для отчетов"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Идентификатор отчета"""
        pass

    @abstractmethod
    def generate(self, data: List[Dict]) -> str:
        """Генерация отчета"""
        pass

    @staticmethod
    def _validate_data(data: List[Dict]) -> None:
        """Валидация входных данных"""
        if not data:
            raise ValueError("Нет данных для отчета")
        required = {'name', 'department', 'hours', 'rate'}
        for i, item in enumerate(data, 1):
            if missing := required - item.keys():
                raise ValueError(f"Запись {i} пропущенных полей: {missing}")
