from urllib.parse import urlsplit, urlunsplit
from .url_rules import COMMON_TLD_TYPOS, COMMON_TLDS

def clean_url(records):
    for record in records:
        original_value = record.get("original_value")

        if original_value is None or not str(original_value).strip():
            record["cleaned_value"] = None
            record["status"] = "Missing"
            record["notes"] = "Original value is empty"
            continue

        notes = []

        try:

            cleaned, whitespace_notes = strip_whitespace(original_value)
            notes.extend(whitespace_notes)

            cleaned, https_notes = add_https(cleaned)
            notes.extend(https_notes)

            cleaned, slashes_notes = fix_scheme_slashes(cleaned)
            notes.extend(slashes_notes)

            cleaned, path_slash_notes = remove_extra_path_slashes(cleaned)
            notes.extend(path_slash_notes)

            cleaned, lowercase_notes = lowercase_scheme_and_domain(cleaned)
            notes.extend(lowercase_notes)

            cleaned, period_notes = remove_extra_domain_periods(cleaned)
            notes.extend(period_notes)

            cleaned, common_tld_notes = fix_common_tld(cleaned)
            notes.extend(common_tld_notes)

            uncommon_tld_flag, uncommon_tld_notes = has_uncommon_tld(cleaned)
            notes.extend(uncommon_tld_notes)

            invalid_url_flag, invalid_url_notes = is_invalid_url(cleaned)
            notes.extend(invalid_url_notes)

        except ValueError:
            notes.append("URL contains an invalid hostname or port")
            record["cleaned_value"] = None
            record["status"] = "Invalid"
            record["notes"] = "; ".join(notes)
            continue
            
        if invalid_url_flag:
            record["cleaned_value"] = None
            record["status"] = "Invalid"
        elif uncommon_tld_flag:
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

def strip_whitespace(url):
    cleaned = url.strip()
    notes = []

    if cleaned != url:
        notes.append("Removed surrounding whitespace")

    return cleaned, notes

def lowercase_scheme_and_domain(url):
    notes = []
    parsed = urlsplit(url)

    cleaned = urlunsplit((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path,
        parsed.query,
        parsed.fragment,
    ))

    if cleaned != url:
        notes.append("Converted URL scheme and domain to lowercase")

    return cleaned, notes

def add_https(url):
    notes = []
    lower_url = url.lower()

    if lower_url.startswith(("https:", "http:")):
        return url, notes

    cleaned = f"https://{url.lstrip('/')}"
    notes.append("Added HTTPS scheme")

    return cleaned, notes

def fix_scheme_slashes(url):
    notes = []
    lower_url = url.lower()

    for scheme in ("https", "http"):
        prefix = f"{scheme}:"

        if lower_url.startswith(prefix):
            remainder = url[len(prefix):].lstrip("/")
            cleaned = f"{scheme}://{remainder}"

            if cleaned != url:
                notes.append("Corrected URL scheme slashes")

            return cleaned, notes

    return url, notes

def remove_extra_path_slashes(url):
    notes = []
    parsed = urlsplit(url)
    cleaned_path = parsed.path

    while "//" in cleaned_path:
        cleaned_path = cleaned_path.replace("//", "/")

    if cleaned_path == parsed.path:
        return url, notes

    cleaned = urlunsplit((
        parsed.scheme,
        parsed.netloc,
        cleaned_path,
        parsed.query,
        parsed.fragment,
    ))

    notes.append("Removed duplicate slashes from URL path")

    return cleaned, notes

def fix_common_tld(url):
    notes = []
    parsed = urlsplit(url)
    hostname = parsed.hostname

    if not hostname or "." not in hostname:
        return url, notes

    domain_parts = hostname.split(".")
    original_tld = domain_parts[-1]
    corrected_tld = COMMON_TLD_TYPOS.get(
        original_tld,
        original_tld,
    )

    if corrected_tld == original_tld:
        return url, notes

    domain_parts[-1] = corrected_tld
    corrected_hostname = ".".join(domain_parts)

    host_position = parsed.netloc.lower().rfind(hostname.lower())

    corrected_netloc = (
        parsed.netloc[:host_position]
        + corrected_hostname
        + parsed.netloc[host_position + len(hostname):]
    )

    cleaned = urlunsplit((
        parsed.scheme,
        corrected_netloc,
        parsed.path,
        parsed.query,
        parsed.fragment,
    ))

    notes.append(
        f"Corrected domain ending: .{original_tld} to .{corrected_tld}"
    )

    return cleaned, notes

def remove_extra_domain_periods(url):
    notes = []
    parsed = urlsplit(url)
    hostname = parsed.hostname

    if not hostname or ".." not in hostname:
        return url, notes

    cleaned_hostname = hostname

    while ".." in cleaned_hostname:
        cleaned_hostname = cleaned_hostname.replace("..", ".")

    cleaned_netloc = parsed.netloc.replace(
        hostname,
        cleaned_hostname,
        1,
    )

    cleaned = urlunsplit((
        parsed.scheme,
        cleaned_netloc,
        parsed.path,
        parsed.query,
        parsed.fragment,
    ))

    notes.append("Removed consecutive periods from domain")

    return cleaned, notes

def has_uncommon_tld(url):
    notes = []
    parsed = urlsplit(url)
    hostname = parsed.hostname

    if not hostname or "." not in hostname:
        return False, notes

    tld = hostname.split(".")[-1].lower()

    if tld not in COMMON_TLDS:
        notes.append(
            f"Potential top-level domain misspelling: .{tld}"
        )
        return True, notes

    return False, notes

def is_invalid_url(url):
    notes = []

    if any(character.isspace() for character in url):
        notes.append("URL contains whitespace")

    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
        parsed.port
    except ValueError:
        notes.append("URL contains an invalid hostname or port")
        return True, notes

    if parsed.scheme not in ("http", "https"):
        notes.append("URL must use HTTP or HTTPS")

    if not hostname:
        notes.append("URL hostname is missing")
        return True, notes

    if "." not in hostname:
        notes.append("URL hostname has no domain ending")

    if ".." in hostname:
        notes.append("URL hostname contains consecutive periods")
    
    if hostname.startswith(".") or hostname.endswith("."):
        notes.append("URL hostname starts or ends with a period")

    for domain_part in hostname.split("."):
        if not domain_part:
            continue

        if domain_part.startswith("-") or domain_part.endswith("-"):
            notes.append("Domain section starts or ends with a hyphen")

        cleaned_part = domain_part.replace("-", "")

        if not cleaned_part.isalnum():
            notes.append("Domain contains invalid characters")

        if len(domain_part) > 63:
            notes.append("Domain section is too long")

    if len(hostname) > 253:
        notes.append("URL hostname is too long")

    return bool(notes), notes