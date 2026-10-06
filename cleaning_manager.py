from cleaners.email_cleaner import clean_email
from cleaners.url_cleaner import clean_url
from cleaners.text_cleaner import clean_text
from cleaners.phone_cleaner import clean_phone
from cleaners.date_cleaner import clean_date


def clean_records(parsed_records, cleaning_type):
    if cleaning_type == "email":
        return clean_email(parsed_records)
    elif cleaning_type == "url":
        return clean_url(parsed_records)
    elif cleaning_type == "phone":
        return clean_phone(parsed_records)
    elif cleaning_type == "text":
        return clean_text(parsed_records)
    elif cleaning_type == "date":
        return clean_date(parsed_records)

    return "Cleaning type not found"