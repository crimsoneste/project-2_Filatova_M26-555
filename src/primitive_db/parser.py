def parse_value(value_str):
    if value_str.lower() == 'true':
        return True
    if value_str.lower() == 'false':
        return False
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    try:
        return int(value_str)
    except ValueError:
        return value_str


def parse_condition(args):
    if len(args) < 3:
        return None
    col = args[0]
    val = parse_value(args[2])
    return {col: val}