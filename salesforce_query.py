import requests

def run_query(access_token, instance_url,query,field_name):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"{instance_url}/services/data/v67.0/query"

    response = requests.get(
        url,
        headers=headers,
        params={"q": query},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    total_size = data["totalSize"]

    print("Status code:", response.status_code)
    print("Total size:", total_size)

    parsed_records = parse_records(data["records"], field_name)

    return parsed_records

def parse_records(records, field_name):
    parsed_records = []
    normalized_field_name = field_name.lower()

    for record in records:
        normalized_record = {
            key.lower(): value
            for key, value in record.items()
        }

        parsed_records.append({
            "id": normalized_record.get("id"),
            "original_value": normalized_record.get(
                normalized_field_name
            ),
        })

    return parsed_records