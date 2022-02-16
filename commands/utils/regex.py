import re

class Regex:
    def __init__(self):
        ...
        
    def email_basic_regex(self, email: str) -> bool:
        regex_result = re.search(r"\S+@\S+", email)
        return regex_result