from .salesforce_authentication import authenticate
from .soql_builder import build_query
from .salesforce_query import run_query 

def get_salesforce_records(keep_missing_values):  
    print("\nSalesforce Data Cleaner")
    print("------------------------")
    
    object_name = input("Object API name: ").strip().lower()
    field_name = input("Field API name: ").strip().lower()

    sorting = input(
        "Sort order [CreatedDate DESC]: "
    ).strip() or "CreatedDate DESC"
    
    record_limit = input(
        "Record limit [all]: "
    ).strip() or "all"

    print("\n=== Run Summary ===")

    access_token,instance_url = authenticate()

    soql_query = build_query(object_name,field_name,sorting,record_limit,keep_missing_values)

    print(f"Running query: {soql_query}")
    returned_records = run_query(access_token,instance_url,soql_query,field_name)
    print("\n")
    return returned_records