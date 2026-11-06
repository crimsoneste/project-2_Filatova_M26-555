ALLOWED_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f"Ошибка: Таблица '{table_name}' уже существует.")
        return False

    for col_name, col_type in columns:
        if col_type not in ALLOWED_TYPES:
            print(f"Ошибка: Недопустимый тип '{col_type}' для столбца '{col_name}'. Разрешены: int, str, bool.")
            return False

    user_provided_id = any(col_name.upper() == "ID" for col_name, _ in columns)

    final_columns = []
    
    # Если пользователь не ввел ID, пишем предупреждение
    if not user_provided_id:
        print("Примечание: Вы не ввели ID, он был сгенерирован автоматически.")
        final_columns.append({"name": "ID", "type": "int"})

    for col_name, col_type in columns:
        final_columns.append({"name": col_name, "type": col_type})

    metadata[table_name] = {"columns": final_columns}
    print(f"Таблица '{table_name}' успешно создана.")
    
    return True


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не найдена.")
        return False

    del metadata[table_name]
    print(f"Таблица '{table_name}' успешно удалена.")
    
    return True