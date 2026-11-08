ALLOWED_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return False

    for col_name, col_type in columns:
        if col_type not in ALLOWED_TYPES:
            print(f"Некорректное значение: {col_type}. Попробуйте снова.")
            return False

    final_columns = [{"name": "ID", "type": "int"}]

    for col_name, col_type in columns:
        if col_name.upper() == "ID":
            continue
        final_columns.append({"name": col_name, "type": col_type})

    metadata[table_name] = {"columns": final_columns}
    
    cols_str = ", ".join([f"{col['name']}:{col['type']}" for col in final_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    
    return True

def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return True


def list_tables(metadata):
    for table_name in metadata.keys():
        print(f"- {table_name}")


def info(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
        
    from .utils import load_table_data
    table_data = load_table_data(table_name)
    
    cols = [f"{c['name']}:{c['type']}" for c in metadata[table_name]['columns']]
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(cols)}")
    print(f"Количество записей: {len(table_data)}")


def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    
    columns = metadata[table_name]['columns']
    
    if len(values) != len(columns) - 1:
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return None

    new_record = {}
    for i, col in enumerate(columns[1:]):
        val_str = values[i]
        try:
            if col['type'] == 'int':
                new_record[col['name']] = int(val_str)
            elif col['type'] == 'bool':
                new_record[col['name']] = val_str.lower() in ('true', '1', 'yes')
            else:
                new_record[col['name']] = str(val_str)
        except ValueError:
            print(f"Некорректное значение: {val_str}. Попробуйте снова.")
            return None

    from .utils import load_table_data
    table_data = load_table_data(table_name)
    
    max_id = max([row["ID"] for row in table_data], default=0)
    new_record["ID"] = max_id + 1
    
    table_data.append(new_record)
    print(f'Запись с ID={new_record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data

def select(table_data, where_clause=None):
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


def update(table_name, table_data, set_clause, where_clause):
    updated_count = 0
    updated_ids = []
    
    for row in table_data:
        match = True
        for key, val in where_clause.items():
            if str(row.get(key)).lower() != str(val).lower():
                match = False
                break
        
        if match:
            updated_ids.append(row['ID'])
            for set_key, set_val in set_clause.items():
                row[set_key] = set_val
            updated_count += 1
            
    if updated_count > 0:
        for uid in updated_ids:
            print(f'Запись с ID={uid} в таблице "{table_name}" успешно обновлена.')
    else:
        print("Записей, удовлетворяющих условию, не найдено.")
        
    return table_data

def delete(table_name, table_data, where_clause):
    new_data = []
    deleted_ids = []
    
    for row in table_data:
        match = True
        for key, val in where_clause.items():
            if str(row.get(key)).lower() != str(val).lower():
                match = False
                break
        
        if match:
            deleted_ids.append(row['ID'])
        else:
            new_data.append(row)
            
    if deleted_ids:
        for did in deleted_ids:
            print(f'Запись с ID={did} успешно удалена из таблицы "{table_name}".')
    else:
        print("Записей, удовлетворяющих условию, не найдено.")
        
    return new_data