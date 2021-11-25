"""Аутентификация — пропускаем сообщения только от одного Telegram аккаунта"""
import datetime
import pytz
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
import db


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if not db.check_value(value=int(message.from_user.id), column='id', table='user_info'):
            user = {'id': int(message.from_user.id),
                    'first_name': str(message.from_user.first_name),
                    'last_name': str(message.from_user.last_name),
                    'username': str(message.from_user.username),
                    'created': datetime.datetime.now(pytz.timezone("Europe/Moscow"))}
            db.insert(table='user_info', column_values=user)
