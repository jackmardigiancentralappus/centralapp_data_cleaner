import re

DEFAULT_COUNTRY_CODE = "1"

DEFAULT_PHONE_OPTIONS = {
    "default_region": DEFAULT_COUNTRY_CODE,
    "output_format": "standard",
    "keep_extension": True,
}

COUNTRY_PHONE_RULES = {
    "1": {
        "country": "US/Canada",
        "pattern": r"^[2-9]\d{2}[2-9]\d{6}$",
    },
    "52": {
        "country": "Mexico",
        "pattern": r"^\d{10}$",
    },
    "44": {
        "country": "United Kingdom",
        "pattern": r"^\d{9,10}$",
    },
    "61": {
        "country": "Australia",
        "pattern": r"^\d{9}$",
    },
}

EXTENSION_PATTERN = re.compile(
    r"\s*(?:ext(?:ension)?\.?|x)\s*(\d+)\s*$",
    re.IGNORECASE,
)
