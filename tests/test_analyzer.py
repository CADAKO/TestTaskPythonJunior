# tests/test_analyzer.py
import pytest
from modules.data_models import DeveloperData, PerformanceReportRow
from modules.report_generators import PerformanceReportGenerator
from modules.utils import load_all_data
from typing import List


@pytest.fixture
def mock_developer_data() -> List[DeveloperData]:
    """Фикстура, возвращающая список объектов DeveloperData."""
    return [
        DeveloperData('Alex', 'Backend Developer', 45, 4.8, 'Python', 'API', 5),
        DeveloperData('Maria', 'Frontend Developer', 38, 4.7, 'React', 'Web',
                      4),
        DeveloperData('Ivan', 'Backend Developer', 30, 4.2, 'Python', 'API', 3),
        DeveloperData('Mike', 'QA Engineer', 41, 4.5, 'Selenium', 'Testing', 4),
    ]


# Используем параметризацию для тестирования разных сценариев
@pytest.mark.parametrize("input_data, expected_output", [
    # Сценарий 1: Основной набор данных
    ([
         DeveloperData('Alex', 'BE', 45, 4.8, '', '', 0),
         DeveloperData('Ivan', 'BE', 30, 4.2, '', '', 0),
         DeveloperData('Mike', 'QA', 41, 4.5, '', '', 0),
     ], [
         PerformanceReportRow('BE', 4.5),
         PerformanceReportRow('QA', 4.5),
     ]),
    # Сценарий 2: Пустые данные
    ([], []),
])
def test_performance_report_generation(input_data, expected_output):
    generator = PerformanceReportGenerator(input_data)
    actual_result = generator.generate()
    assert actual_result == expected_output


def test_load_data_minimal(tmp_path):
    # Используем dataclass для ожидаемого результата
    expected_result = [
        DeveloperData(name='John Doe', position='Developer', completed_tasks=0,
                      performance=4.5, skills='', team='', experience_years=0),
    ]

    csv_content = "name,position,completed_tasks,performance,skills,team," \
                  "experience_years\nJohn Doe,Developer,0,4.5,,,0\n "
    temp_file = tmp_path / "test_data.csv"
    temp_file.write_text(csv_content, encoding='utf-8')

    raw_data = load_all_data([str(temp_file)])
    assert raw_data == expected_result


def test_load_invalid_path():
    invalid_path = ['employees0.csv']
    with pytest.raises(SystemExit) as excinfo:
        load_all_data(invalid_path)
    assert excinfo.value.code == 1
