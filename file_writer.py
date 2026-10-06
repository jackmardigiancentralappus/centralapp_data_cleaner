import csv

from pathlib import Path

def create_output_file(records, output_file, keep_unchanged_values, keep_missing_values):
    if not output_file.endswith(".csv"):
        output_file += ".csv"

    output_file = Path(__file__).resolve().parent / "output_file" / Path(output_file).name
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Salesforce ID",
            "Original Value",
            "Cleaned Value",
            "Status",
            "Notes",
        ])

        for record in records:
            if (
                (keep_unchanged_values == "y" or record.get("status") != "Unchanged")
                and
                (keep_missing_values == "y" or record.get("status") != "Missing")
            ):
                writer.writerow([
                    record.get("id"),
                    record.get("original_value"),
                    record.get("cleaned_value"),
                    record.get("status"),
                    record.get("notes"),
                ])

    return output_file