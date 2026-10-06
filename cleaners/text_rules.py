DEFAULT_TEXT_OPTIONS = {
    "trim_whitespace": False,
    "collapse_spaces": False,
    "remove_html": False,
    "capitalization_type": "none",
    "preset_regex_types": [],
    "custom_regex_pattern": None,
    "custom_regex_replacement": "",
}

COMMON_REGEX_PRESETS = {
    "remove_numbers": {
        "pattern": r"\d+",
        "replacement": "",
        "description": "Remove all numbers",
    },

    "keep_numbers_only": {
        "pattern": r"\D+",
        "replacement": "",
        "description": "Remove everything except numbers",
    },

    "remove_punctuation": {
        "pattern": r"[^\w\s]",
        "replacement": "",
        "description": "Remove punctuation and special characters",
    },

    "remove_line_breaks": {
        "pattern": r"[\r\n]+",
        "replacement": " ",
        "description": "Replace line breaks with spaces",
    },

    "remove_tabs": {
        "pattern": r"\t+",
        "replacement": " ",
        "description": "Replace tabs with spaces",
    },

    "collapse_repeated_punctuation": {
        "pattern": r"([.!?,])\1+",
        "replacement": r"\1",
        "description": "Collapse repeated punctuation",
    },

    "remove_email_addresses": {
        "pattern": r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
        "replacement": "",
        "description": "Remove email addresses from text",
    },

    "remove_urls": {
        "pattern": r"https?://\S+|www\.\S+",
        "replacement": "",
        "description": "Remove URLs from text",
    },

    "remove_parentheses": {
        "pattern": r"[()]",
        "replacement": "",
        "description": "Remove parentheses but preserve their contents",
    },

    "remove_parenthetical_text": {
        "pattern": r"\([^)]*\)",
        "replacement": "",
        "description": "Remove text contained in parentheses",
    },
}