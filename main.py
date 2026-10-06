from salesforce_authentication import authenticate
from soql_builder import build_query
from salesforce_query import run_query
from cleaning_manager import clean_records
from file_writer import create_output_file
from pathlib import Path

def main() -> None:
    print("\nSalesforce Data Cleaner")
    print("------------------------")
    
    object_name = input("Object API name: ").strip().lower()
    field_name = input("Field API name: ").strip().lower()
    cleaning_type = input("Cleaning type: ").strip().lower()
    keep_unchanged_values = input("Keep unchanged values (Y/N) [Y]: ").strip().lower() or "y"
    keep_missing_values = input("Keep missing values (Y/N) [Y]: ").strip().lower() or "y"

    sorting = input(
        "Sort order [CreatedDate DESC]: "
    ).strip() or "CreatedDate DESC"
    
    record_limit = input(
        "Record limit [all]: "
    ).strip() or "all"

    output_file = input(
        "Output filename [cleaned_data.xlsx]: "
    ).strip() or "cleaned_data.xlsx"

    print("\n=== Run Summary ===")

    access_token,instance_url = authenticate()

    soql_query = build_query(object_name,field_name,sorting,record_limit)

    print(f"Running query: {soql_query}")
    returned_records = run_query(access_token,instance_url,soql_query,field_name)
    print("\n")
    cleaned_records = clean_records(returned_records,cleaning_type)

    final_output_file = create_output_file(cleaned_records,output_file, keep_unchanged_values, keep_missing_values)

    print(f"\nOutput saved to: {Path(output_file).resolve()}")

if __name__ == "__main__":
    main()