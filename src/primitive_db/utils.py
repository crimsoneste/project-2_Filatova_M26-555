"""Вспомогательные функции для работы с файловой системой
(загрузка/сохранение метаданных и данных таблиц)"""

import json
import os


def load_metadata(filepath):
    """Загрузка данных из JSON-файла"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохранение переданных данных в JSON-файл"""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_table_data(table_name):
    """Загрузка данные конкретной таблицы в указанную директорию"""
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохранение данные конкретной таблицы в указанную директорию"""
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
