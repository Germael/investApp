import re


def camel_to_snake(name: str) -> str:
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def price_change(first, second):
    return ((first - second) / second) * 100
