from cleaners import email_cleaner


class TestRemoveExtraAtSigns:
    def test_remove_extra_at_signs(self):
        bad_email = "testemail@@@gmail.com"
        cleaned_email, notes = email_cleaner.remove_extra_at_signs(bad_email)

        assert cleaned_email == "testemail@gmail.com"
        assert "Removed excess @ signs" in notes

    def test_single_at_sign_is_unchanged(self):
        normal_email = "testemail@gmail.com"
        cleaned_email, notes = email_cleaner.remove_extra_at_signs(normal_email)

        assert cleaned_email == normal_email
        assert not notes


class TestFixCommonDomain:
    def test_common_domain_typos_are_corrected(self):
        emails = []
        cases = {
            "test@gamil.com": "test@gmail.com",
            "test@yaho.com": "test@yahoo.com",
            "test@hotnail.com": "test@hotmail.com",
            "test@outlok.com": "test@outlook.com",
            "test@iclud.com": "test@icloud.com",
        }
        
        for original_email, expected_email in cases.items():
            cleaned_email, notes = email_cleaner.fix_common_domain(original_email)

            assert cleaned_email == expected_email
            assert notes
    
    def test_correct_domains_are_not_changed(self):
        emails = []
        cases = {
            "test@gmail.com",
            "test@yaho0.com",
            "test@hotmail.com",
            "test@outlook.com",
            "test@icloud.com"
        }
        
        for original_email in cases:
            cleaned_email, notes = email_cleaner.fix_common_domain(original_email)

            assert cleaned_email == original_email
            assert not notes


class TestIsSuspiciousEmail:
    def test_suspicious_flag_set(self):
        email = "fake@gmail.com"
        suspicious, notes = email_cleaner.is_suspicious_email(email)

        assert suspicious
        assert "Suspicious email username or domain" in notes

    def test_suspicious_flag_not_set(self):
        email = "johnsmith@gmail.com"
        suspicious, notes = email_cleaner.is_suspicious_email(email)

        assert not suspicious
        assert not notes


class TestStripWhitespace:
    def test_removed_whitespace(self):
        email = " test@gmail.com "
        cleaned, notes = email_cleaner.strip_whitespace(email)

        assert cleaned != email
        assert "Removed surrounding whitespace" in notes

    def test_no_whitespace_removed(self):
        email = "test@gmail.com"
        cleaned, notes = email_cleaner.strip_whitespace(email)

        assert cleaned == email
        assert not notes

class TestChangeToLowercase:
    def test_set_to_lowercase(self):
        email = " TEST@GMAIL.COM "
        cleaned, notes = email_cleaner.change_to_lowercase(email)

        assert cleaned != email
        assert "Converted to lowercase" in notes

    def test_already_lowercase(self):
        email = "test@gmail.com"
        cleaned, notes = email_cleaner.change_to_lowercase(email)

        assert cleaned == email
        assert not notes


class TestIsInvalidEmail:
    def test_no_username(self):
        email = "@gmail.com"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email username is missing" in notes

    def test_no_domain(self):
        email = "test@"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email domain is missing" in notes

    def test_contains_spaces(self):
        email = "test @gmail.com"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email contains spaces" in notes

    def test_no_extension(self):
        email = "test@gmail"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email domain has no extension" in notes

    def test_username_starts_or_ends_with_period(self):
        email = "test.@gmail.com"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email username starts or ends with a period" in notes

    def test_domain_starts_or_ends_with_period(self):
        email = "test@.gmail.com"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email domain starts or ends with a period" in notes

    def test_consecutive_periods(self):
        email = "test@gmail..com"
        cleaned, notes = email_cleaner.is_invalid_email(email)

        assert cleaned != email
        assert "Email contains consecutive periods" in notes
    
    def test_valid_email(self):
        email = "test@gmail.com"
        valid, notes = email_cleaner.is_invalid_email(email)

        assert not valid
        assert not notes