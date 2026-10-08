from cleaning_manager import clean_records
from file_writer import create_output_file
from pathlib import Path
from input_sources.salesforce.salesforce_input import get_salesforce_records
from input_sources.file.file_input import get_file_records
from user_input import (ask_choice, ask_yes_no, ask_number, ask_text)

def main() -> None:

    print("CentralApp Data Cleaner")
    print("------------------------")

    record_source = ask_choice("What source does the data originate from (Salesforce/File): ", ["salesforce", "file"], "salesforce")
    cleaning_type = ask_choice("What cleaning type would like to perform (Email/Phone/URL/Text/Date/Address): ", ["email","phone","url","text","date","address"])
    output_file = ask_text("Output filename [cleaned_data.csv]:", "cleaned_data.csv")
    keep_unchanged_values = ask_yes_no("Keep unchanged values (Y/N) [N]: ", "n")
    keep_missing_values = ask_yes_no("Keep missing values (Y/N) [N]: ", "n")

    if record_source == "salesforce":
        returned_records = get_salesforce_records(keep_missing_values)
    elif record_source == "file":
        returned_records = get_file_records()
    else:
        raise ValueError(f"Unsupported source: {record_source}")
    
    cleaned_records = clean_records(returned_records,cleaning_type)

    final_output_file = create_output_file(cleaned_records,output_file, keep_unchanged_values, keep_missing_values)

    print(f"\nOutput saved to: {Path(final_output_file).resolve()}")

if __name__ == "__main__":
    main()