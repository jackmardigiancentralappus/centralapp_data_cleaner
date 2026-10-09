import re
from datetime import datetime

from .date_rules import DATE_FORMATS, DEFAULT_DATE_FORMAT
from user_input import ask_choice

def clean_date(records):
    options = run_date_inputs()

    for record in records:
        original_value = record.get("original_value")
        notes = []

        if original_value is None or not str(original_value).strip():
            record["cleaned_value"] = None
            record["status"] = "Missing"
            record["notes"] = "Original value is empty"
            continue

        original_value = str(original_value)
        cleaned = original_value

        invalid_date_flag, invalid_character_notes = has_invalid_characters(cleaned)
        notes.extend(invalid_character_notes)

        if invalid_date_flag:
            record["cleaned_value"] = None
            record["status"] = "Invalid"

        else:
            cleaned, whitespace_notes = strip_whitespace(cleaned)
            notes.extend(whitespace_notes)

            try:
                cleaned, format_notes = apply_date_format(
                    cleaned, options["current_format"], options["output_format"]
                )
            except ValueError:
                record["cleaned_value"] = None
                record["status"] = "Invalid"
                notes.append(f"Invalid date for format {options['current_format']}")
                record["notes"] = "; ".join(notes)
                continue
            notes.extend(format_notes)

            if cleaned != original_value:
                record["cleaned_value"] = cleaned
                record["status"] = "Cleaned"
            else:
                record["cleaned_value"] = None
                record["status"] = "Unchanged"

        record["notes"] = "; ".join(notes) if notes else None

    return records

def strip_whitespace(date_value):
    notes = []
    original = str(date_value)
    cleaned = original.strip()

    if cleaned != original:
        notes.append("Removed surrounding whitespace")

    return cleaned, notes


def has_invalid_characters(date_value):
    invalid_pattern = r"[^0-9./\s-]"
    invalid_date = bool(re.search(invalid_pattern, date_value))

    notes = ["Invalid characters present"] if invalid_date else []
    return invalid_date, notes

def apply_date_format(date_value, current_format, output_format=DEFAULT_DATE_FORMAT):
    current_format = current_format.strip().upper()
    output_format = output_format.strip().upper()

    if current_format not in DATE_FORMATS:
        raise ValueError(f"Unsupported current date format: {current_format}")
    if output_format not in DATE_FORMATS:
        raise ValueError(f"Unsupported output date format: {output_format}")

    parsed_date = datetime.strptime(date_value, DATE_FORMATS[current_format])
    cleaned = parsed_date.strftime(DATE_FORMATS[output_format])

    notes = []
    if cleaned != date_value:
        notes.append(f"Changed date format to {output_format}")

    return cleaned, notes


def run_date_inputs():

    options = {}
    format_choices = ["yyyy-mm-dd", "dd/mm/yyyy", "mm/dd/yyyy"]

    print("\nOutput format examples:")
    print("YYYY-MM-DD: 2026-06-12")
    print("DD/MM/YYYY:   12/06/2026")
    print("MM/DD/YYYY:   06/12/2026")
    print()

    options["current_format"] = ask_choice("What is the current date format (YYYY-MM-DD || DD/MM/YYYY || MM/DD/YYYY) [YYYY-MM-DD]: ", format_choices , "yyyy-mm-dd").upper()
    options["output_format"] = ask_choice("Desired output format (YYYY-MM-DD || DD/MM/YYYY || MM/DD/YYYY) [YYYY-MM-DD]: ", format_choices , "yyyy-mm-dd").upper()

    return options
