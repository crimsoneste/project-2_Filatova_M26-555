"""Реализация декораторов для обработки ошибок, подтверждений и логирования"""

import time
from functools import wraps


def handle_db_errors(func):
    """Перехватыват и обработка ошибок базы данных"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. Возможно, " \
                "база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name):
    """Запрос у пользователя подтверждения перед выполнением небезопасной операции"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirm = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            if confirm.lower() != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Отсчет и вывод времени выполнения функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд")
        return result

    return wrapper


def create_cacher():
    """Создание функции-замыкания для кэширования результатов запросов"""
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result
