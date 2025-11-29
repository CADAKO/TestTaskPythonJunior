import argparse
import csv
import collections
import sys
import tabulate
from operator import itemgetter


def create_parser():
    parser = argparse.ArgumentParser(description='parser for report')
    parser.add_argument('--files', nargs='+', type=str,
                        help='Files for analyze', required=True)
    parser.add_argument('--report', type=str, help='Type of report',
                        default='performance', required=True)
    return parser


def generate_performance_report(all_raw_data):
    performance_summary = collections.defaultdict(list)
    final_perf = []
    for row in all_raw_data:
        performance_summary[row['position']].append(float(row['performance']))
    for items in performance_summary.items():
        average = sum(items[1]) / len(items[1])
        final_perf.append({'position': items[0],
                           'performance': round(average, 2)})
    final_perf.sort(key=itemgetter('performance'), reverse=True)
    return final_perf


def load_all_data(file_paths):
    all_raw_data = []
    for files in file_paths:
        try:
            with open(files, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    all_raw_data.append(row)
        except FileNotFoundError:
            print(f"Error: File not found at {file_paths}", file=sys.stderr)
            sys.exit(1)
    return all_raw_data


def display_report(report_type, all_data):
    report_handlers = {
        'performance': generate_performance_report,
    }
    if report_type in report_handlers:
        handler = report_handlers[report_type]
        final_report_data = handler(all_data)
        row_index = [i + 1 for i in range(len(final_report_data))]
        print(tabulate.tabulate(final_report_data, headers='keys',
                                showindex=row_index, floatfmt=".2f"))
    else:
        print(f"Error: Unknown report type '{report_type}'. Available types: "
              f"{list(report_handlers.keys())}")
        sys.exit(1)


def main():
    parser = create_parser()
    args = parser.parse_args()
    all_data = load_all_data(args.files)
    display_report(args.report, all_data)


if __name__ == '__main__':
    main()
