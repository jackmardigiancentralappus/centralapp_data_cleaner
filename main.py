from cleaning_manager import clean_records
from file_writer import create_output_file
from pathlib import Path
from input_sources.salesforce.salesforce_input import get_salesforce_records
from input_sources.file.file_input import get_file_records

def main() -> None:

    print("CentralApp Data Cleaner")
    print("------------------------")

    record_source = input("What source does the data originate from (Salesforce/File) [Salesforce]").strip().lower()  or "salesforce"
    cleaning_type = input("Cleaning type: ").strip().lower()
    output_file = input("Output filename [cleaned_data.csv]: ").strip() or "cleaned_data.csv"
    keep_unchanged_values = input("Keep unchanged values (Y/N) [Y]: ").strip().lower() or "y"
    keep_missing_values = input("Keep missing values (Y/N) [Y]: ").strip().lower() or "y"

    if record_source == "salesforce":
        returned_records = get_salesforce_records()
    elif record_source == "file":
        returned_records = get_file_records()
    else:
        raise ValueError(f"Unsupported source: {record_source}")
    
    cleaned_records = clean_records(returned_records,cleaning_type)

    final_output_file = create_output_file(cleaned_records,output_file, keep_unchanged_values, keep_missing_values)

    print(f"\nOutput saved to: {Path(final_output_file).resolve()}")

if __name__ == "__main__":
    main()