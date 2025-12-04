# modules/main.py
import argparse
import sys
from tabulate import tabulate
from modules.utils import load_all_data
from modules.report_generators import PerformanceReportGenerator
from modules.data_models import DeveloperData, PerformanceReportRow
from typing import List


def create_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Analyze developers performance and generate reports.')
    parser.add_argument(
        '--files',
        type=str,
        nargs='+',
        required=True,
        help="List of input CSV files paths."
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        # Используем choices для валидации аргумента --report
        choices=['performance'],
        help="Type of report to generate. Available: performance."
    )
    return parser


def process_and_display_report(report_type: str, all_data: List[DeveloperData]):
    """Выбирает нужный обработчик отчета, генерирует данные и выводит их."""

    if report_type == 'performance':
        generator = PerformanceReportGenerator(all_data)
        report_data = generator.generate()
        row_index = [i + 1 for i in range(len(report_data))]
        # tabulate отлично работает со списками dataclasses
        print(tabulate(report_data, headers="keys", showindex=row_index,
                       floatfmt=".2f"))
    else:
        # Эта ветка больше недостижима благодаря choices в argparse,
        # но оставлена для примера расширяемости
        print(f"Error: Unknown report type '{report_type}'", file=sys.stderr)
        sys.exit(1)


def main():
    """Основная точка входа в скрипт."""
    parser = create_parser()
    args = parser.parse_args()

    all_data = load_all_data(args.files)

    process_and_display_report(args.report, all_data)


if __name__ == "__main__":
    main()
