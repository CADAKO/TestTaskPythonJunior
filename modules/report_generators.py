# modules/report_generators.py
from abc import ABC, abstractmethod
from typing import List
from collections import defaultdict
from modules.data_models import DeveloperData, PerformanceReportRow
import operator


class BaseReportGenerator(ABC):
    """Абстрактный базовый класс для генераторов отчетов."""

    def __init__(self, data: List[DeveloperData]):
        self.data = data

    @abstractmethod
    def generate(self) -> List[PerformanceReportRow]:
        """Генерирует и возвращает отсортированный отчет."""
        pass


class PerformanceReportGenerator(BaseReportGenerator):
    """Генератор отчета по средней эффективности."""

    def generate(self) -> List[PerformanceReportRow]:
        if not self.data:
            return []

        performance_by_position = defaultdict(list)
        for dev in self.data:
            performance_by_position[dev.position].append(dev.performance)

        average_performance_data = []
        for position, scores in performance_by_position.items():
            avg_score = sum(scores) / len(scores)
            average_performance_data.append(
                PerformanceReportRow(
                    position=position,
                    average_performance=round(avg_score, 2)
                )
            )

        # Сортировка по убыванию
        sorted_report = sorted(average_performance_data,
                               key=operator.attrgetter('average_performance'),
                               reverse=True)

        return sorted_report
