import csv
from user_input import (ask_number)

def parse_csv_records(file_path):

    with open(file_path, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        header = next(file_reader, None)
        if header is None:
            raise ValueError("The CSV file is empty.")

        header_count = 0
        print("\nColumn Headers")
        for column_header in header:
            header_count += 1
            print(f"\n {header_count}: {column_header}")
        
        id_index = ask_number("ID column number: ", 1, header_count) - 1
        value_index = ask_number("Column to clean: ", 1, header_count) - 1

        records = []
        for row in file_reader:
            records.append({
                "id": row[id_index],
                "original_value": row[value_index],
            })

        return records

