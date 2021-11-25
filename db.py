import os
from typing import Dict, List, Tuple
from xlsxwriter.workbook import Workbook
import sqlite3

conn = sqlite3.connect(os.path.join("db", "finance.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetchandgroupall(table: str, column: str, groupeby: str, user) -> List[Tuple]:
    cursor.execute(f"SELECT {column} FROM {table} where user_id = {user} group by {groupeby}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[0])
    return result


def get_all_categories(user: int):
    """Возвращает список всех категорий пользователя"""
    cursor.execute(f"SELECT upper(category) FROM expense where user_id = {user} group by category")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[0])
    return result


def check_value(value: int, column: str, table: str):
    """Проверяет наличие значения в таблике по условию"""
    cursor.execute(f"SELECT {column} FROM {table} where {column} = {value}")
    rows = cursor.fetchall()
    if not rows:
        return None
    return True


def delete(table: str, row_id: int) -> None:
    """Удаляет расход по его id."""
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r", encoding='utf-8') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


def export(user):
    """Возвращает все расходы пользователя в файле Excell."""
    filename = 'export/expense.xlsx'
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()
    mysel = cursor.execute(
        f"select date(created), amount, upper(category), description from expense where user_id = {user}")
    title = [["Дата", "Сумма", "Категория", "Описание"]]
    for i, row in enumerate(title):
        for j, value in enumerate(row):
            worksheet.write(i, j, row[j])
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i + 1, j, row[j])
    workbook.close()
    return filename


check_db_exists()
