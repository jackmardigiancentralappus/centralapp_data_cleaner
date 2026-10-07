from pathlib import Path
from .csv_handler import parse_csv_records
from .excel_handler import parse_excel_records
import csv

def get_file_records():
    print("\nFile Data Cleaner")
    print("------------------------")

    file_path = Path(
        input("Path to file: ").strip().strip('"')
    ).expanduser()

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.suffix.lower():
        raise ValueError("Please choose a file.")
    else:
        suffix = file_path.suffix.lower()

    if suffix == ".csv":
        return parse_csv_records(file_path)
    elif suffix == '.xlsx':
        return parse_excel_records(file_path)
    else:
        raise ValueError("Invalid file suffix")