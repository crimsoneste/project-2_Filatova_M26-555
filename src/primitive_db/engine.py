"""Основной цикл, обработка ввода пользователя и вызов команд"""

import shlex

from prettytable import PrettyTable

from decorators import create_cacher
from primitive_db.constants import META_FILE
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_condition
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Выводит справочную информацию по доступным командам."""
    print("\n***Операции с данными***\n")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...)"
        " - создать запись"
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение>"
        " - прочитать записи по условию"
    )
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print(
        "<command> update <имя_таблицы> set <столбец1>" \
        " = <новое_значение1> where <столбец_условия> = <значение> - обновить"
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение>"
        " - удалить запись"
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Запускает основной цикл программы."""
    print_help()

    select_cache = create_cacher()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = input("Введите команду: ").strip()

        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0].lower()

        try:
            if command == "exit":
                break

            elif command == "help":
                print_help()

            elif command == "create_table":
                if len(args) < 3:
                    continue
                table_name = args[1]
                columns = []
                for arg in args[2:]:
                    if ":" in arg:
                        name, col_type = arg.split(":", 1)
                        columns.append((name, col_type))
                if create_table(metadata, table_name, columns):
                    save_metadata(META_FILE, metadata)

            elif command == "drop_table":
                if len(args) == 2:
                    if drop_table(metadata, args[1]):
                        save_metadata(META_FILE, metadata)

            elif command == "list_tables":
                list_tables(metadata)

            elif command == "info":
                if len(args) == 2:
                    info_table(metadata, args[1])

            elif command == "insert":
                if len(args) > 4 and args[1] == "into" and args[3] == "values":
                    table_name = args[2]
                    values_str = " ".join(args[4:]).strip("()")
                    values = [v.strip() for v in values_str.split(",")]

                    new_data = insert(metadata, table_name, values)
                    if new_data is not None:
                        save_table_data(table_name, new_data)
                        select_cache = create_cacher()

            elif command == "select":
                if len(args) > 2 and args[1] == "from":
                    table_name = args[2]
                    table_data = load_table_data(table_name)

                    where_clause = None
                    if len(args) > 4 and args[3] == "where":
                        where_clause = parse_condition(args[4:])

                    cache_key = f"{table_name}_{str(where_clause)}"
                    result = select_cache(
                        cache_key, lambda: select(table_data, where_clause)
                    )

                    if result:
                        table = PrettyTable()
                        table.field_names = [
                            c["name"] for c in metadata[table_name]["columns"]
                        ]
                        for row in result:
                            table.add_row(
                                [
                                    row.get(c["name"])
                                    for c in metadata[table_name]["columns"]
                                ]
                            )
                        print(table)
                    else:
                        print("Записей не найдено.")

            elif command == "update":
                if len(args) > 5:
                    table_name = args[1]
                    if "set" in args and "where" in args:
                        set_idx = args.index("set")
                        where_idx = args.index("where")

                        set_clause = parse_condition(args[set_idx + 1 : where_idx])
                        where_clause = parse_condition(args[where_idx + 1 :])

                        table_data = load_table_data(table_name)
                        new_data = update(
                            table_name, table_data, set_clause, where_clause
                        )
                        save_table_data(table_name, new_data)
                        select_cache = create_cacher()

            elif command == "delete":
                if len(args) > 4 and args[1] == "from" and args[3] == "where":
                    table_name = args[2]
                    where_clause = parse_condition(args[4:])

                    table_data = load_table_data(table_name)
                    new_data = delete(table_name, table_data, where_clause)
                    if new_data is not None:
                        save_table_data(table_name, new_data)
                        select_cache = create_cacher()

            else:
                print(f"Функции {command} нет. Попробуйте снова.")

        except Exception:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
