import re

from .phone_rules import (
    COUNTRY_PHONE_RULES,
    DEFAULT_COUNTRY_CODE,
    DEFAULT_PHONE_OPTIONS,
    EXTENSION_PATTERN,
)

def clean_phone(records):
    options = run_phone_inputs()

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

        cleaned, whitespace_notes = strip_whitespace(cleaned)
        notes.extend(whitespace_notes)

        cleaned, simple_typo_notes = correct_simple_typos(cleaned)
        notes.extend(simple_typo_notes)

        cleaned, extension, extension_notes = apply_extension_option(
            cleaned, options["keep_extension"]
        )
        notes.extend(extension_notes)

        invalid_phone_flag, invalid_character_notes = has_invalid_characters(cleaned)
        notes.extend(invalid_character_notes)

        if not invalid_phone_flag:
            country_code = determine_country_code(cleaned)
            invalid_phone_flag, invalid_phone_notes = is_invalid_phone(cleaned, country_code)
            notes.extend(invalid_phone_notes)

        if invalid_phone_flag:
            record["cleaned_value"] = None
            record["status"] = "Invalid"
        else:
            cleaned = format_phone(cleaned, country_code, options["output_format"])
            if extension is not None:
                cleaned = f"{cleaned} ext. {extension}"

            if cleaned != original_value:
                record["cleaned_value"] = cleaned
                record["status"] = "Cleaned"
            else:
                record["cleaned_value"] = None
                record["status"] = "Unchanged"

        record["notes"] = "; ".join(notes) if notes else None

    return records

def strip_whitespace(phone_number):
    notes = []
    cleaned = str(phone_number).strip()
    if cleaned != phone_number:
        notes.append("Removed whitespace")
    return cleaned, notes

def has_invalid_characters(phone_number):
    notes = []
    invalid_pattern = r"[^0-9+().\-\s]"
    invalid_phone = bool(re.search(invalid_pattern, phone_number))
    if invalid_phone:
        notes.append("Invalid characters present")

    return invalid_phone, notes

def correct_simple_typos(phone_number):
    notes = []
    cleaned = phone_number

    normalized = re.sub(r"[\u2010-\u2015\u2212]", "-", cleaned)

    if normalized != cleaned:
        notes.append("Normalized dash characters")

    cleaned = normalized

    collapsed = re.sub(
        r"([().-])\1+",
        r"\1",
        cleaned,
    )

    if collapsed != cleaned:
        notes.append("Collapsed repeated phone punctuation")

    return collapsed, notes

def determine_country_code(phone_number):

    has_plus_prefix = phone_number.startswith("+")
    digits = re.sub(r"\D", "", phone_number)
    
    has_international_prefix = has_plus_prefix or digits.startswith("00")

    if digits.startswith("00"):
        digits = digits[2:]

    country_codes = sorted(COUNTRY_PHONE_RULES, key=len, reverse=True,)

    for country_code in country_codes:
        if digits.startswith(country_code):
            if has_international_prefix:
                return country_code

            national_number = digits[len(country_code):]
            country_pattern = COUNTRY_PHONE_RULES[country_code]["pattern"]

            if re.fullmatch(country_pattern, national_number):
                return country_code

        continue

    return DEFAULT_COUNTRY_CODE

def is_invalid_phone(phone_number, country_code):
    notes = []

    country_rule = COUNTRY_PHONE_RULES.get(country_code)

    if country_rule is None:
        notes.append(f"Unsupported country code: {country_code}")
        return True, notes

    digits = re.sub(r"\D", "", phone_number)
    has_plus_prefix = phone_number.startswith("+")
    has_double_zero_prefix = digits.startswith("00")

    if has_double_zero_prefix:
        digits = digits[2:]

    has_explicit_country_code = (
        has_plus_prefix or has_double_zero_prefix
    )

    if has_explicit_country_code:
        if digits.startswith(country_code):
            digits = digits[len(country_code):]
    elif digits.startswith(country_code):
        number_without_country_code = digits[len(country_code):]
        country_pattern = country_rule["pattern"]

        if re.fullmatch(country_pattern, number_without_country_code):
            digits = number_without_country_code

    country_pattern = country_rule["pattern"]
    invalid_phone = not bool(
        re.fullmatch(country_pattern, digits)
    )

    if invalid_phone:
        country_name = country_rule["country"]
        notes.append(
            f"Phone number does not match the {country_name} format"
        )

    return invalid_phone, notes

def format_phone(phone_number, country_code, output_format):
    """Format a validated number, keeping international codes when requested."""
    digits = re.sub(r"\D", "", phone_number)
    if digits.startswith("00"):
        digits = digits[2:]

    country_rule = COUNTRY_PHONE_RULES[country_code]
    national_number = digits
    if digits.startswith(country_code):
        remainder = digits[len(country_code):]
        if re.fullmatch(country_rule["pattern"], remainder):
            national_number = remainder

    if output_format == "e164":
        return f"+{country_code}{national_number}"

    if country_code == "1":
        if output_format == "standard":
            return f"({national_number[:3]}) {national_number[3:6]}-{national_number[6:]}"
        if output_format == "dashes":
            return f"{national_number[:3]}-{national_number[3:6]}-{national_number[6:]}"

    if output_format == "digits":
        return national_number if country_code == "1" else f"{country_code}{national_number}"

    # No national grouping rules are defined for the other supported countries.
    if output_format == "dashes":
        return f"+{country_code}-{national_number}"
    return f"+{country_code} {national_number}"

def apply_extension_option(phone_number, keep_extension):
    notes = []
    match = EXTENSION_PATTERN.search(phone_number)

    if match is None:
        return phone_number, None, notes

    phone_without_extension = phone_number[:match.start()].rstrip()
    extension = match.group(1)

    if keep_extension:
        notes.append("Preserved phone extension")
        return phone_without_extension, extension, notes

    notes.append("Removed phone extension")
    return phone_without_extension, None, notes

def run_phone_inputs():
    options = DEFAULT_PHONE_OPTIONS.copy()

    print("\nOutput format examples:")
    print("Standard: (555) 123-4567")
    print("Dashes:   555-123-4567")
    print("Digits:   5551234567")
    print("E164:     +15551234567")
    print()

    options["output_format"] = input(
        "Output format (Standard/Dashes/Digits/E164) [Standard]: "
    ).strip().lower() or "standard"
    if options["output_format"] not in {"standard", "dashes", "digits", "e164"}:
        raise ValueError("Output format must be Standard, Dashes, Digits, or E164")

    options["keep_extension"] = (
        input("Keep phone extensions (Y/N) [Y]: ").strip().lower()
        or "y"
    ) in ("y", "yes")

    return options
