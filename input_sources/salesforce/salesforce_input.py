from .salesforce_authentication import authenticate
from .soql_builder import build_query
from .salesforce_query import run_query 
from user_input import (ask_choice,ask_yes_no,ask_text)

def get_salesforce_records(keep_missing_values):  
    print("\nSalesforce Data Cleaner")
    print("------------------------")
    
    object_name = ask_text("Object API name: ")
    field_name = ask_text("Field API name: ")

    sorting = ask_text("Sort order [CreatedDate DESC]: ", "createddate")
    
    while True:
        record_limit = input("Record limit [all]: ").strip().lower() or "all"
        if record_limit == "all" or (record_limit.isdigit() and int(record_limit) > 0):
            break
        print("  Please enter a number, or press Enter for all.")

    print("\n=== Run Summary ===")

    access_token,instance_url = authenticate()

    soql_query = build_query(object_name,field_name,sorting,record_limit,keep_missing_values)

    print(f"Running query: {soql_query}")
    returned_records = run_query(access_token,instance_url,soql_query,field_name)
    print("\n")
    return returned_records