import re
from .text_rules import DEFAULT_TEXT_OPTIONS, COMMON_REGEX_PRESETS
from user_input import (ask_choice,ask_yes_no)

def clean_text(records):
    options = run_text_inputs()

    for record in records:
        text_value = record.get("original_value")

        if text_value is None or not str(text_value).strip():
            record["cleaned_value"] = None
            record["status"] = "Missing"
            record["notes"] = "Original value is empty"
            continue

        notes = []

        if options["trim_whitespace"]:
            text_value,whitespace_notes = strip_whitespace(text_value)
            notes.extend(whitespace_notes)

        if options["collapse_spaces"]:
            text_value,collapse_spaces_notes = collapse_extra_spaces(text_value)
            notes.extend(collapse_spaces_notes)
        if options["remove_html"]:
            text_value,remove_html_notes = remove_html_tags(text_value)
            notes.extend(remove_html_notes)
        
        if options["capitalization_type"] != "none":
            text_value,capitalization_notes = correct_capitalization(text_value,options["capitalization_type"])
            notes.extend(capitalization_notes)

        for preset_name in options["preset_regex_types"]:
            preset = COMMON_REGEX_PRESETS.get(preset_name)

            if preset is None:
                notes.append(f"Unknown regex preset: {preset_name}")
                continue

            text_value, preset_notes = run_regex(
                text_value,
                preset["pattern"],
                preset["replacement"],
                f"Applied regex preset: {preset_name}",
            )

            notes.extend(preset_notes)

        if options["custom_regex_pattern"]:
            text_value, custom_regex_notes = run_regex(
                text_value,
                options["custom_regex_pattern"],
                options["custom_regex_replacement"],
                "Applied custom regex",
            )

            notes.extend(custom_regex_notes)



        if text_value != record.get("original_value"):
            record["cleaned_value"] = text_value
            record["status"] = "Cleaned"
            

        else:
            record["cleaned_value"] = None
            record["status"] = "Unchanged"

        record["notes"] = "; ".join(notes) if notes else None

    return records

def strip_whitespace(text):
    cleaned = text.strip()
    notes = []

    if cleaned != text:
        notes.append("Removed surrounding whitespace")

    return cleaned, notes

def collapse_extra_spaces(text):
    notes = []
    cleaned = re.sub(r" {2,}", " ", text)

    if cleaned != text:
        notes.append("Collapsed repeated spaces")

    return cleaned, notes

def remove_html_tags(text):
    notes = []
    clean_pattern = re.compile(r'<.*?>')
    cleaned = re.sub(clean_pattern, '', text)
    if cleaned != text:
        notes.append("Removed HTML tags")
    return cleaned, notes

def correct_capitalization(text,capitalization_type):
    notes = []
    cleaned = text

    if capitalization_type == 'upper':
        cleaned = cleaned.upper()
        if cleaned != text:
            notes.append("Capitalized every character in string")
    elif capitalization_type == 'lower':
        cleaned = cleaned.lower()
        if cleaned != text:
            notes.append("Lowercased every character in string")
    elif capitalization_type == 'title':
        cleaned = re.sub(r'\b[a-zA-Z][a-zA-Z0-9]*', lambda m: m.group(0)[:1].upper() + m.group(0)[1:], text)
        if cleaned != text:
            notes.append("Capitalized every word in string")
    elif capitalization_type == 'sentence':
        cleaned = re.sub(r'(^|[.!?]\s*)([a-zA-Z])', lambda m: m.group(1) + m.group(2).upper(), text)
        if cleaned != text:
            notes.append("Capitalized every sentence in string")

    return cleaned,notes

def run_regex(text, regex_pattern, replacement, note):
    notes = []
    clean_pattern = re.compile(regex_pattern)
    cleaned = re.sub(clean_pattern, replacement, text)

    if cleaned != text:
        notes.append(note)

    return cleaned, notes

def run_text_inputs():
    text_mode = ask_choice("Mode (Preset/Custom/Both): ", ["preset", "custom", "both"])

    print(f"{text_mode} selected\n")

    options = DEFAULT_TEXT_OPTIONS.copy()
    if text_mode in ("preset", "both"):
        options["trim_whitespace"] = ask_yes_no("Trim whitespace (Y/N): " , "y")
        options["collapse_spaces"] = ask_yes_no("Collapse spaces (Y/N): " , "y")
        options["remove_html"] = ask_yes_no("Remove HTML tags (Y/N): " , "y")
        options["capitalization_type"] = ask_choice("Capitalization (Upper/Lower/Title/Sentence/None) [None]: ", ["upper", "lower", "title", "sentence", "none"], "none")

        print("\nAvailable regex presets:")

        for preset_name, preset in COMMON_REGEX_PRESETS.items():
            print(f"- {preset_name}: {preset['description']}")

        while True:
            selected = input("\nEnter preset names separated by commas [none]: ").strip().lower()
            names = [name.strip() for name in selected.split(",") if name.strip()]
            unknown = [name for name in names if name not in COMMON_REGEX_PRESETS]
            if not unknown:
                options["preset_regex_types"] = names
                break
            print(f"  Unknown preset(s): {', '.join(unknown)}")

    if text_mode in ("custom", "both"):
        while True:
            pattern = input("Regex pattern: ")
            try:
                re.compile(pattern)
                break
            except re.error as e:
                print(f"  That pattern isn't valid ({e}). Try again.")
        options["custom_regex_pattern"] = pattern

        options["custom_regex_replacement"] = input(
            "Replace matches with [nothing]: "
        )

    return options