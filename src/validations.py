import re

def is_unique(data, field, value):
    for item in data:
        if item[field] == value:
            return False
    return True

def valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def valid_year(year):
    return year in (1, 2, 3)

def not_empty(text):
    return isinstance(text, str) and len(text.strip()) > 0
