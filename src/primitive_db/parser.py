"""Функции для разбора сложных команд (where, set, values)"""


def parse_value(value_str):
    """Преобразует строковое значение в правильный тип данных (int, bool или str)"""
    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False
    if (value_str.startswith('"') and value_str.endswith('"')) or (
        value_str.startswith("'") and value_str.endswith("'")
    ):
        return value_str[1:-1]
    try:
        return int(value_str)
    except ValueError:
        return value_str


def parse_condition(args):
    """Преобразует список аргументов вида ['age', '=', '28'] в словарь {'age': 28}"""
    if len(args) < 3:
        return None
    col = args[0]
    val = parse_value(args[2])
    return {col: val}
