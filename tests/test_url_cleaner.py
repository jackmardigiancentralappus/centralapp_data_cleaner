from cleaners import url_cleaner


class TestStripWhitespace:
    def test_removed_whitespace(self):
        url = " www.google.com "
        cleaned, notes = url_cleaner.strip_whitespace(url)

        assert cleaned != url
        assert "Removed surrounding whitespace" in notes

    def test_no_whitespace_removed(self):
        url = "www.google.com"
        cleaned, notes = url_cleaner.strip_whitespace(url)

        assert cleaned == url
        assert not notes


class TestLowercaseSchemeAndDomain:
    def test_set_to_lowercase(self):
        url = "HTTPS://WWW.GOOGLE.COM"
        cleaned, notes = url_cleaner.lowercase_scheme_and_domain(url)

        assert cleaned != url
        assert "Converted URL scheme and domain to lowercase" in notes

    def test_already_lowercase(self):
        url = "https://www.google.com"
        cleaned, notes = url_cleaner.lowercase_scheme_and_domain(url)

        assert cleaned == url
        assert not notes


class TestAddHttps:
    def test_no_https(self):
        url = "www.google.com"
        cleaned, notes = url_cleaner.add_https(url)

        assert cleaned != url
        assert "Added HTTPS scheme" in notes

    def test_https_already_exists(self):
        url = "https://www.google.com"
        cleaned, notes = url_cleaner.add_https(url)

        assert cleaned == url
        assert not notes


class TestFixSchemeSlashes:
    def test_too_many_slashes(self):
        url = "https:///www.google.com"
        cleaned, notes = url_cleaner.fix_scheme_slashes(url)

        assert cleaned != url
        assert "Corrected URL scheme slashes" in notes

    def test_no_slashes(self):
        url = "https:www.google.com"
        cleaned, notes = url_cleaner.fix_scheme_slashes(url)

        assert cleaned != url
        assert "Corrected URL scheme slashes" in notes

    def test_correct_amount_of_slashes(self):
        url = "https://www.google.com"
        cleaned, notes = url_cleaner.fix_scheme_slashes(url)

        assert cleaned == url
        assert not notes

class TestRemoveExtraPath_Slashes:
    def test_too_many_slashes(self):
        url = "https://www.google.com///images"
        cleaned, notes = url_cleaner.remove_extra_path_slashes(url)

        assert cleaned != url
        assert "Removed duplicate slashes from URL path" in notes

    def test_correct_amount_of_slashes(self):
        url = "https://www.google.com/images"
        cleaned, notes = url_cleaner.remove_extra_path_slashes(url)

        assert cleaned == url
        assert not notes


class TestFixCommonTld:
    def test_common_typo(self):
        url = "https://www.google.comm/images"
        cleaned, notes = url_cleaner.fix_common_tld(url)

        assert cleaned != url
        assert "Corrected domain ending: .comm to .com" in notes

    def test_correct_spelling(self):
        url = "https://www.google.com/images"
        cleaned, notes = url_cleaner.fix_common_tld(url)

        assert cleaned == url
        assert not notes

class TestRemoveExtraDomainPeriods:
    def test_common_typo(self):
        url = "https://www..google.com/images"
        cleaned, notes = url_cleaner.remove_extra_domain_periods(url)

        assert cleaned != url
        assert "Removed consecutive periods from domain" in notes

    def test_correct_spelling(self):
        url = "https://www.google.com/images"
        cleaned, notes = url_cleaner.remove_extra_domain_periods(url)

        assert cleaned == url
        assert not notes

class TestHasUncommonTld:
    def test_common_typo(self):
        url = "https://www..google.juz/images"
        uncommon_tld_flag, notes = url_cleaner.has_uncommon_tld(url)

        assert uncommon_tld_flag == True
        assert "Potential top-level domain misspelling: .juz" in notes

    def test_correct_spelling(self):
        url = "https://www.google.com/images"
        uncommon_tld_flag, notes = url_cleaner.has_uncommon_tld(url)

        assert uncommon_tld_flag == False
        assert not notes

class TestIsInvalidUrl:
    def test_invalid_scheme(self):
        url = "ftp://www.google.com"

        invalid_url_flag, notes = url_cleaner.is_invalid_url(url)

        assert invalid_url_flag is True
        assert "URL must use HTTP or HTTPS" in notes

    def test_missing_domain_ending(self):
        url = "https://localhost"

        invalid_url_flag, notes = url_cleaner.is_invalid_url(url)

        assert invalid_url_flag is True
        assert "URL hostname has no domain ending" in notes

    def test_valid_url(self):
        url = "https://www.google.com/images"

        invalid_url_flag, notes = url_cleaner.is_invalid_url(url)

        assert invalid_url_flag is False
        assert notes == []