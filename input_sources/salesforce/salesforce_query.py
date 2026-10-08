import requests

"""
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
"""

def run_query(access_token, instance_url, query, field_name):
    headers = {"Authorization": f"Bearer {access_token}"}
    base_url = instance_url.rstrip("/")
    url = f"{base_url}/services/data/v67.0/query"
    params = {"q": query}

    records = []
    total_size = None
    visited_urls = set()

    while True:
        if url in visited_urls:
            raise RuntimeError("Salesforce returned a repeated pagination URL.")
        visited_urls.add(url)

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        if total_size is None:
            total_size = data["totalSize"]

        records.extend(data["records"])

        if data["done"] is True:
            break

        next_url = data.get("nextRecordsUrl")
        if not next_url:
            raise RuntimeError(
                "Salesforce reported more records but omitted nextRecordsUrl."
            )

        url = f"{base_url}/{next_url.lstrip('/')}"
        params = None  # The next-page URL already identifies the query.

    if len(records) != total_size:
        raise RuntimeError(
            f"Incomplete Salesforce download: expected {total_size} "
            f"records, retrieved {len(records)}."
        )

    print(f"Retrieved {len(records)} of {total_size} records.")
    return parse_records(records, field_name)

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