# modules/utils.py
import csv
import sys
from typing import List
from modules.data_models import DeveloperData


def load_all_data(file_paths: List[str]) -> List[DeveloperData]:
    """Загружает данные из всех указанных файлов и
    возвращает список объектов DeveloperData."""
    all_raw_data = []
    for file_path in file_paths:
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Приводим типы и создаем объект dataclass
                    dev_data = DeveloperData(
                        name=row['name'],
                        position=row['position'],
                        completed_tasks=int(row['completed_tasks']),
                        performance=float(row['performance']),
                        skills=row['skills'],
                        team=row['team'],
                        experience_years=int(row['experience_years'])
                    )
                    all_raw_data.append(dev_data)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}", file=sys.stderr)
            sys.exit(1)
        except (ValueError, TypeError, KeyError) as e:
            print(f"Warning: Skipping row due to data error in file "
                  f"{file_path}: {e}", file=sys.stderr)

    return all_raw_data
