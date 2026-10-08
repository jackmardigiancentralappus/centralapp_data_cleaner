import pytest

from cleaners import phone_cleaner


@pytest.mark.parametrize(
    ("output_format", "expected"),
    [
        ("standard", "(555) 234-5678"),
        ("dashes", "555-234-5678"),
        ("digits", "5552345678"),
        ("e164", "+15552345678"),
    ],
)
def test_output_formats(monkeypatch, output_format, expected):
    monkeypatch.setattr(
        phone_cleaner,
        "run_phone_inputs",
        lambda: {"output_format": output_format, "keep_extension": True},
    )
    records = [{"original_value": "555–234–5678"}]

    result = phone_cleaner.clean_phone(records)[0]

    assert result["cleaned_value"] == expected
    assert result["status"] == "Cleaned"
    assert "Normalized dash characters" in result["notes"]


@pytest.mark.parametrize("keep_extension", [True, False])
def test_extension_preference(monkeypatch, keep_extension):
    monkeypatch.setattr(
        phone_cleaner,
        "run_phone_inputs",
        lambda: {"output_format": "e164", "keep_extension": keep_extension},
    )

    result = phone_cleaner.clean_phone(
        [{"original_value": " 555-234-5678 ext. 42 "}]
    )[0]

    expected = "+15552345678 ext. 42" if keep_extension else "+15552345678"
    assert result["cleaned_value"] == expected
    assert result["status"] == "Cleaned"
    assert ("Preserved" if keep_extension else "Removed") + " phone extension" in result["notes"]


def test_international_number_and_invalid_number(monkeypatch):
    monkeypatch.setattr(
        phone_cleaner,
        "run_phone_inputs",
        lambda: {"output_format": "e164", "keep_extension": True},
    )
    records = [
        {"original_value": "+44 1234 567890"},
        {"original_value": "555-234-5678 xabc"},
        {"original_value": None},
    ]

    results = phone_cleaner.clean_phone(records)

    assert results[0]["cleaned_value"] == "+441234567890"
    assert results[1]["status"] == "Invalid"
    assert results[1]["cleaned_value"] is None
    assert results[2]["status"] == "Missing"


@pytest.mark.parametrize(
    ("output_format", "expected"),
    [
        ("standard", "+44 1234567890"),
        ("dashes", "+44-1234567890"),
        ("digits", "441234567890"),
        ("e164", "+441234567890"),
    ],
)
def test_international_formats(monkeypatch, output_format, expected):
    monkeypatch.setattr(
        phone_cleaner,
        "run_phone_inputs",
        lambda: {"output_format": output_format, "keep_extension": True},
    )

    result = phone_cleaner.clean_phone(
        [{"original_value": "+44 1234 567890"}]
    )[0]

    assert result["cleaned_value"] == expected
    assert result["status"] == "Cleaned"


def test_already_formatted_number_is_unchanged(monkeypatch):
    monkeypatch.setattr(
        phone_cleaner,
        "run_phone_inputs",
        lambda: {"output_format": "standard", "keep_extension": True},
    )

    result = phone_cleaner.clean_phone(
        [{"original_value": "(555) 234-5678"}]
    )[0]

    assert result["status"] == "Unchanged"
    assert result["cleaned_value"] is None
