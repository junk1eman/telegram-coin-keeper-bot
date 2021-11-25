""" Работа с расходами — их добавление, удаление, статистики"""
import datetime
import re
from typing import List, NamedTuple, Optional
import pytz
import db
import exceptions


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str
    description: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str, user: int) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category": parsed_message.category_text.upper(),
        "description": parsed_message.description,
        "raw_text": raw_message,
        "user_id": user
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=parsed_message.category_text)


def get_today_statistics(user: str) -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount)"
                   f"from expense where date(created)=date('now', 'localtime') and user_id = {user}"
                   )
    result = cursor.fetchone()
    if not result:
        return "Сегодня ещё нет расходов"
    else:
        all_today_expenses = result[0]
        return (f"Расходы сегодня:\n"
                f"всего — {all_today_expenses} руб.\n"
                f"За текущий месяц: /month")


def get_month_statistics(user) -> str:
    """Возвращает строкой статистику расходов за текущий месяц"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select category, sum(amount) "
                   f"from expense where date(created) >= '{first_day_of_month}'"
                   f"and user_id = {user} "
                   f"group by category "
                   f"order by sum(amount) DESC")
    result = cursor.fetchall()
    if not result:
        return "В этом месяце ещё нет расходов"
    sum_expense = 0
    all_today_expenses = "Расходы в текущем месяце:\n\n"
    for expense in result:
        sum_expense += int(expense[1])
        all_today_expenses += expense[0] + ": " + str(expense[1]) + " руб.\n"
    all_today_expenses += "\nВсего: " + str(sum_expense) + " руб."
    return all_today_expenses


def last(user) -> List[Expense]:
    """Возвращает последние несколько расходов"""
    cursor = db.get_cursor()
    cursor.execute(
        f"select id, amount, category "
        f"from expense "
        f"where user_id = {user} "
        f"order by created desc limit 10")
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def delete_expense(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    db.delete("expense", row_id)


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\-\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")

    search_description = re.match(r"(.*)\.(.*)", regexp_result.group(2))

    amount = regexp_result.group(1).replace(" ", "")

    if not search_description or not search_description.group(0) \
            or not search_description.group(1) or not search_description.group(2):
        description = None
        category_text = regexp_result.group(2).strip().lower()
    else:
        description = search_description.group(2).strip().lower()
        category_text = search_description.group(1).strip().lower()

    return Message(amount=int(amount), category_text=category_text, description=description)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now
