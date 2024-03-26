from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from services import DataBase

db = DataBase()


class UserBannedMiddleware(BaseMiddleware):
    
    """
    Промежуточное программное обеспечение для проверки статуса пользователя.
    
    Перед обработкой каждого сообщения, колбэк-запроса или инлайн-запроса проверяет,
    не заблокирован ли пользователь. Если пользователь заблокирован, обработка запроса прекращается,
    и пользователю отправляется сообщение о блокировке.
    """
    
    async def on_process_message(self, message: Message, data: dict):
        
        """
        Обрабатывает входящие сообщения.

        Параметры:
        - message (Message): Объект сообщения от пользователя.
        - data (dict): Словарь с дополнительными данными.
        
        Проверяет статус пользователя в базе данных. Если пользователь заблокирован,
        отправляет ему сообщение о блокировке и прекращает обработку сообщения.
        """
        
        try:
            user = await db.status(message.from_user.id)
        except:
            user = 'user'
        if user == 'ban':
            if message.chat.type == 'private':
                await message.answer(
                '*You are banned please contact to @eckorezze for more information!*', parse_mode="MarkdownV2"
            )
            raise CancelHandler

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        
        """
        Обрабатывает входящие колбэк-запросы.

        Параметры:
        - call (CallbackQuery): Объект колбэк-запроса от пользователя.
        - data (dict): Словарь с дополнительными данными.
        
        Аналогично методу on_process_message, проверяет статус пользователя и, при необходимости,
        информирует его о блокировке, прекращая дальнейшую обработку запроса.
        """
        
        user = await db.status(call.from_user.id)
        if user == 'ban':
            await call.answer(
                'You are banned please contact to @eckorezze for more information!',
                show_alert=True
            )
            raise CancelHandler

    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        
        """
        Обрабатывает входящие инлайн-запросы.

        Параметры:
        - query (InlineQuery): Объект инлайн-запроса от пользователя.
        - data (dict): Словарь с дополнительными данными.
        
        Проверяет, не заблокирован ли пользователь, и в случае блокировки прекращает обработку запроса.
        """
        
        user = await db.status(query.from_user.id)
        if user == 'ban':
            raise CancelHandler


def setup_ban_middleware(dp: Dispatcher):
    
    """
    Регистрирует промежуточное программное обеспечение проверки блокировки пользователя в диспетчере.

    Параметры:
    - dp (Dispatcher): Экземпляр диспетчера Aiogram.
    """
    
    dp.middleware.setup(UserBannedMiddleware())


def setup_ban_middlewares(dp: Dispatcher):
    
    """
    Вспомогательная функция для регистрации всех необходимых промежуточных программных обеспечений.

    Параметры:
    - dp (Dispatcher): Экземпляр диспетчера Aiogram.
    
    В текущей реализации регистрирует только middleware проверки блокировки пользователя.
    """
    
    setup_ban_middleware(dp)
