# modules/data_models.py
from dataclasses import dataclass


@dataclass
class DeveloperData:
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: str
    team: str
    experience_years: int


@dataclass
class PerformanceReportRow:
    position: str
    average_performance: float
