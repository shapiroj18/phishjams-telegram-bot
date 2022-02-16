from commands.utils.regex import Regex

regex = Regex()


def test_email_basic_regex_success():
    assert regex.email_basic_regex("shapiroj18@gmail.com") is not None


def test_email_basic_regex_fail():
    assert regex.email_basic_regex("notanemail") is None
