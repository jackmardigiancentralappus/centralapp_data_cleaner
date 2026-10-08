from .email_rules import (COMMON_DOMAIN_TYPOS,SUSPICIOUS_DOMAINS,SUSPICIOUS_USERNAMES,)
import math

def clean_email(records):
    for record in records:
        original_value = record.get("original_value")

        if original_value is None or not str(original_value).strip():
            record["cleaned_value"] = None
            record["status"] = "Missing"
            record["notes"] = "Original value is empty"
            continue

        notes = []

        cleaned, whitespace_notes = strip_whitespace(original_value)
        notes.extend(whitespace_notes)

        cleaned, lowercase_notes = change_to_lowercase(cleaned)
        notes.extend(lowercase_notes)

        cleaned, extra_at_signs_notes = remove_extra_at_signs(cleaned)
        notes.extend(extra_at_signs_notes)

        cleaned, fix_common_domain_notes = fix_common_domain(cleaned)
        notes.extend(fix_common_domain_notes)

        suspicious_email, suspicious_notes = is_suspicious_email(cleaned)
        notes.extend(suspicious_notes)

        invalid_email, invalid_notes = is_invalid_email(cleaned)
        notes.extend(invalid_notes)

        #entropy_flag, entropy_notes = check_email_entropy(cleaned)
        #notes.extend(entropy_notes)

        if invalid_email:
            record["cleaned_value"] = None
            record["status"] = "Invalid"

        #elif entropy_flag:
            #record["cleaned_value"] = None
            #record["status"] = "Review"

        elif suspicious_email:
            record["cleaned_value"] = None
            record["status"] = "Review"
        elif cleaned != original_value:
            record["cleaned_value"] = cleaned
            record["status"] = "Cleaned"

        else:
            record["cleaned_value"] = None
            record["status"] = "Unchanged"

        record["notes"] = "; ".join(notes) if notes else None

    return records


def remove_extra_at_signs(email):
    notes = []
    cleaned = email

    while "@@" in cleaned:
        cleaned = cleaned.replace("@@", "@")

    if cleaned != email:
        notes.append("Removed excess @ signs")

    return cleaned, notes


def fix_common_domain(email):
    notes = []

    if email.count("@") != 1:
        return email, notes

    username, domain = email.split("@")
    final_domain = COMMON_DOMAIN_TYPOS.get(domain, domain)
    cleaned = f"{username}@{final_domain}"

    if final_domain != domain:
        notes.append(f"Corrected domain typo: {domain} to {final_domain}")

    return cleaned, notes


def is_suspicious_email(email):
    notes = []

    if email.count("@") != 1:
        return False, notes

    username, domain = email.lower().split("@")

    suspicious = (
        username in SUSPICIOUS_USERNAMES
        or domain in SUSPICIOUS_DOMAINS
    )

    if suspicious:
        notes.append("Suspicious email username or domain")

    return suspicious, notes

def strip_whitespace(email):
    cleaned = email.strip()
    notes = []

    if cleaned != email:
        notes.append("Removed surrounding whitespace")

    return cleaned, notes

def change_to_lowercase(email):
    cleaned = email.lower()
    notes = []

    if cleaned != email:
        notes.append("Converted to lowercase")

    return cleaned, notes

def is_invalid_email(email):
    notes = []

    if email.count("@") != 1:
        notes.append("Email must contain exactly one @ sign")
        return True, notes

    username, domain = email.split("@")

    if not username:
        notes.append("Email username is missing")

    if not domain:
        notes.append("Email domain is missing")

    if " " in email:
        notes.append("Email contains spaces")

    if domain and "." not in domain:
        notes.append("Email domain has no extension")

    if username.startswith(".") or username.endswith("."):
        notes.append("Email username starts or ends with a period")

    if domain.startswith(".") or domain.endswith("."):
        notes.append("Email domain starts or ends with a period")

    if ".." in email:
        notes.append("Email contains consecutive periods")

    return bool(notes), notes

"""
def check_email_entropy(email):
    notes = []
    if email.count("@") != 1:
        return False, notes
        
    entropy_flag = False
    username = email.split("@")[0]
    domain = email.split("@")[1]   
    string_list = []
    string_list.append(username)
    string_list.append(domain)

    for string in string_list:
        frequencies = {}
        for char in string:
            frequencies[char] = frequencies.get(char, 0) + 1

        total_chars = len(string)
        entropy = 0.0
        
        for count in frequencies.values():
            probability = count / total_chars
            entropy -= probability * math.log2(probability)

        if entropy <= 1.5:
            entropy_flag = True
            notes.append("Entropy too low. To many repeated characters")
        elif entropy <= 3.4:
            entropy_flag = False
        elif entropy >= 3.5:
            entropy_flag = True
            notes.append("Entropy too high. To many random characters")
        if entropy_flag:
            return entropy_flag, notes
    return entropy_flag, notes
"""