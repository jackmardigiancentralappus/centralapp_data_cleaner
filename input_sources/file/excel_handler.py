from openpyxl import load_workbook
from user_input import (ask_number)


def parse_excel_records(file_path):
    workbook = load_workbook(file_path, read_only=True, data_only=True)
    try:
        rows = workbook.active.iter_rows(values_only=True)
        header = next(rows, None)
        if header is None:
            raise ValueError("The Excel sheet is empty.")

        for number, name in enumerate(header, start=1):
            print(f"{number}: {name}")

        id_index = ask_number("ID column number: ", 1, len(header)) - 1
        value_index = ask_number("Column to clean: ", 1, len(header)) - 1

        return [
            {
                "id": str(row[id_index]) if row[id_index] is not None else None,
                "original_value": str(row[value_index]) if row[value_index] is not None else None,
            }
            for row in rows
        ]
    finally:
        workbook.close()