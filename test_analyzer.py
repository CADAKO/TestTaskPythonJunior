import pytest
from main import display_report, create_parser, generate_performance_report, \
    load_all_data
import math


@pytest.fixture
def mock_raw_data():
    return [
        {'name': 'Alex', 'position': 'Backend Developer', 'completed_tasks':
            '45', 'performance': '4.8', 'skills': 'Python', 'team': 'API',
         'experience_years': '5'},
        {'name': 'Maria', 'position': 'Frontend Developer', 'completed_tasks':
            '38', 'performance': '4.7', 'skills': 'React', 'team': 'Web',
         'experience_years': '4'},
        {'name': 'Ivan', 'position': 'Backend Developer', 'completed_tasks':
            '30', 'performance': '4.2', 'skills': 'Python', 'team': 'API',
         'experience_years': '3'},
        {'name': 'Mike', 'position': 'QA Engineer', 'completed_tasks':
            '41', 'performance': '4.5', 'skills': 'Selenium', 'team':
             'Testing', 'experience_years': '4'},
    ]


# 2. Пишем тестовый случай (test case)
def test_performance_report_generation(mock_raw_data):
    expected_result = [
        {'position': 'Frontend Developer', 'performance': 4.7},
        {'position': 'Backend Developer', 'performance': 4.5},
        {'position': 'QA Engineer', 'performance': 4.5},
    ]

    actual_result = generate_performance_report(mock_raw_data)
    assert len(actual_result) == len(expected_result)

    for i in range(len(expected_result)):
        assert actual_result[i]['position'] == expected_result[i]['position']
        assert math.isclose(actual_result[i]['performance'],
                            expected_result[i]['performance'])


def test_performance_zero_report_generation_empty_input():
    raw_data = []
    expected_result = []

    actual_result = generate_performance_report(raw_data)
    assert actual_result == expected_result


def test_load_data(tmp_path):
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,4.6,"Swift, Kotlin, React Native, iOS",Mobile Team,3
Elena Popova,Backend Developer,43,4.8,"Java, Spring Boot, MySQL, Redis",API Team,4"""
    temp_file = tmp_path / "test_employees.csv"
    temp_file.write_text(csv_content, encoding='utf-8')
    expected_result = [
        {'name': 'David Chen', 'position': 'Mobile Developer',
         'completed_tasks': '36', 'performance': '4.6',
         'skills': 'Swift, Kotlin, React Native, iOS', 'team': 'Mobile Team',
         'experience_years': '3'},
        {'name': 'Elena Popova', 'position': 'Backend Developer',
         'completed_tasks': '43', 'performance': '4.8',
         'skills': 'Java, Spring Boot, MySQL, Redis', 'team': 'API Team',
         'experience_years': '4'}]
    raw_data = load_all_data([str(temp_file)])
    assert len(expected_result) == len(raw_data)
    assert expected_result == raw_data


def test_load_invalid_path():
    invalid_path = ['employees0.csv']
    with pytest.raises(SystemExit) as excinfo:
        load_all_data(invalid_path)
    assert excinfo.value.code == 1


def test_parser_parses_arguments_correctly():
    test_args_list = ['--files', 'file1.csv', 'file2.csv', '--report',
                      'performance']
    parser = create_parser()
    args = parser.parse_args(test_args_list)
    assert args.files == ['file1.csv', 'file2.csv']
    assert args.report == 'performance'


def test_process_and_display_report_performance(mock_raw_data, capsys):
    display_report('performance', mock_raw_data)
    captured = capsys.readouterr()
    assert "Backend Developer" in captured.out
    assert "4.50" in captured.out


def test_process_and_display_report_invalid_type(capsys):
    with pytest.raises(SystemExit) as excinfo:
        display_report('invalid_report',
                       [])  # Пустые данные, так как мы тестируем ветку else

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Unknown report type" in captured.out
