# cleaners/email_rules.py

COMMON_DOMAIN_TYPOS = {
    # Gmail
    "gamil.com": "gmail.com",
    "gmial.com": "gmail.com",
    "gmal.com": "gmail.com",
    "gmai.com": "gmail.com",
    "gmil.com": "gmail.com",
    "gmali.com": "gmail.com",
    "gmaill.com": "gmail.com",
    "gnail.com": "gmail.com",

    # Yahoo
    "yaho.com": "yahoo.com",
    "yahooo.com": "yahoo.com",
    "yhoo.com": "yahoo.com",
    "yaoo.com": "yahoo.com",
    "yahho.com": "yahoo.com",
    "yhaoo.com": "yahoo.com",

    # Hotmail
    "hotnail.com": "hotmail.com",
    "hotmai.com": "hotmail.com",
    "hotmal.com": "hotmail.com",
    "hotmil.com": "hotmail.com",
    "hotmaill.com": "hotmail.com",
    "homtail.com": "hotmail.com",
    "hotamil.com": "hotmail.com",

    # Outlook
    "outlok.com": "outlook.com",
    "outloo.com": "outlook.com",
    "outlookk.com": "outlook.com",
    "outllook.com": "outlook.com",
    "otulook.com": "outlook.com",

    # iCloud
    "iclud.com": "icloud.com",
    "icould.com": "icloud.com",
    "icloudd.com": "icloud.com",
}


SUSPICIOUS_USERNAMES = {
    "fake",
    "test",
    "testing",
    "test123",
    "dummy",
    "sample",
    "example",
    "invalid",
    "noemail",
    "no-email",
    "none",
    "null",
    "unknown",
    "missing",
    "placeholder",
    "notprovided",
    "123",
    "1234",
    "12345",
    "0000",
    "1111",
    "abc",
    "abc123",
    "asdf",
    "qwerty",
}


SUSPICIOUS_DOMAINS = {
    "fake.com",
    "test.com",
    "testing.com",
    "dummy.com",
    "sample.com",
    "invalid.com",
    "noemail.com",
    "none.com",
    "unknown.com",
    "example.com",
    "example.org",
    "example.net",
    "localhost",
}