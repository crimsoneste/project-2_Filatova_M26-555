"""Основная бизнес-логика (создание/удаление таблиц, CRUD-операции)"""

from decorators import confirm_action, handle_db_errors, log_time
from primitive_db.constants import VALID_TYPES
from primitive_db.utils import load_table_data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает новую таблицу в метаданных"""
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    for col_name, col_type in columns:
        if col_type not in VALID_TYPES:
            raise ValueError(
                f"Недопустимый тип {col_type} для столбца {col_name}. "
                f"Разрешены: {', '.join(VALID_TYPES)}."
            )

    final_columns = [{"name": "ID", "type": "int"}]
    for col_name, col_type in columns:
        if col_name.upper() != "ID":
            final_columns.append({"name": col_name, "type": col_type})

    metadata[table_name] = {"columns": final_columns}
    cols_str = ", ".join([f"{col['name']}:{col['type']}" for col in final_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return True


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных"""
    if table_name not in metadata:
        raise KeyError(f'"{table_name}"')
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return True


@handle_db_errors
def list_tables(metadata):
    """Выводит список всех существующих таблиц"""
    if not metadata:
        print("Таблиц нет.")
        return
    for table_name in metadata.keys():
        print(f"- {table_name}")


@handle_db_errors
def info_table(metadata, table_name):
    """Выводит информацию о структуре таблицы"""
    if table_name not in metadata:
        raise KeyError(f'"{table_name}"')

    table_data = load_table_data(table_name)
    cols = [f"{c['name']}:{c['type']}" for c in metadata[table_name]["columns"]]
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(cols)}")
    print(f"Количество записей: {len(table_data)}")


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу"""
    if table_name not in metadata:
        raise KeyError(f'"{table_name}"')

    columns = metadata[table_name]["columns"]
    if len(values) != len(columns) - 1:
        raise ValueError(
            f"Некорректное количество значений. Ожидается {len(columns) - 1}."
        )

    new_record = {}
    for i, col in enumerate(columns[1:]):
        val_str = values[i]
        if col["type"] == "int":
            new_record[col["name"]] = int(val_str)
        elif col["type"] == "bool":
            new_record[col["name"]] = val_str.lower() in ("true", "1", "yes")
        else:
            new_record[col["name"]] = str(val_str)

    table_data = load_table_data(table_name)
    max_id = max([row["ID"] for row in table_data], default=0)
    new_record["ID"] = max_id + 1
    table_data.append(new_record)
    print(f'Запись с ID={new_record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает записи, соответствующие условию (или все)"""
    if not where_clause:
        return table_data
    result = []
    for row in table_data:
        match = True
        for key, val in where_clause.items():
            if str(row.get(key)).lower() != str(val).lower():
                match = False
                break
        if match:
            result.append(row)
    return result


@handle_db_errors
def update(table_name, table_data, set_clause, where_clause):
    """Обновляет записи в таблице по заданному условию"""
    updated_ids = []
    for row in table_data:
        match = True
        for key, val in where_clause.items():
            if str(row.get(key)).lower() != str(val).lower():
                match = False
                break
        if match:
            updated_ids.append(row["ID"])
            for set_key, set_val in set_clause.items():
                row[set_key] = set_val

    if updated_ids:
        for uid in updated_ids:
            print(f'Запись с ID={uid} в таблице "{table_name}" успешно обновлена.')
    else:
        print("Записей, удовлетворяющих условию, не найдено.")
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_name, table_data, where_clause):
    """Удаляет записи из таблицы по заданному условию"""
    new_data = []
    deleted_ids = []
    for row in table_data:
        match = True
        for key, val in where_clause.items():
            if str(row.get(key)).lower() != str(val).lower():
                match = False
                break
        if match:
            deleted_ids.append(row["ID"])
        else:
            new_data.append(row)

    if deleted_ids:
        for did in deleted_ids:
            print(f'Запись с ID={did} успешно удалена из таблицы "{table_name}".')
    else:
        print("Записей, удовлетворяющих условию, не найдено.")
    return new_data
