import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table

DB_FILE = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print("Первая попытка запустить проект!")
    print_help()
    
    while True:
        metadata = load_metadata(DB_FILE)
        
        user_input = input("\nВведите команду: ").strip()
        if not user_input:
            continue
            
        args = shlex.split(user_input)
        command = args[0].lower()

        if command == "exit":
            break
            
        elif command == "help":
            print_help()
            
        elif command == "create":
            if len(args) < 3:
                print("Ошибка: используйте 'create <table_name> <col1:type> <col2:type>...'")
                continue
                
            table_name = args[1]
            columns = []
            is_valid = True
            
            for arg in args[2:]:
                if ":" not in arg:
                    print(f"Ошибка формата: '{arg}'. Ожидается 'имя:тип' (например, age:int).")
                    is_valid = False
                    break
                name, col_type = arg.split(":", 1)
                columns.append((name, col_type))
                
            if is_valid:
                if create_table(metadata, table_name, columns):
                    save_metadata(DB_FILE, metadata)
                    
        elif command == "drop":
            if len(args) != 2:
                print("Ошибка: используйте 'drop <table_name>'")
                continue
                
            table_name = args[1]
            if drop_table(metadata, table_name):
                save_metadata(DB_FILE, metadata)
                
        else:
            print(f"Неизвестная команда: '{command}'. Введите 'help' для справки.")