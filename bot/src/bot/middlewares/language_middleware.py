from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from config import I18N_DOMAIN, LOCALES_DIR
from services import DataBase

db = DataBase()


async def get_lang(user_id):
    
    """
    Получает предпочитаемый язык пользователя из базы данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - Строку с кодом языка, если язык найден, иначе None.
    """
    
    try:
        language = await db.get_language(user_id)
        if language:
            return language
    except:
        pass


class ACLMiddleware(I18nMiddleware):
    
    """
    Промежуточное программное обеспечение для определения языка пользователя.
    
    Расширяет стандартный I18nMiddleware, переопределяя метод получения локали пользователя.
    Определяет язык, используемый в интерфейсе пользователя, на основе данных из базы данных
    или использует локаль пользователя по умолчанию.
    """
    
    async def get_user_locale(self, action, args):
        
        """
        Определяет локаль пользователя.

        Параметры:
        - action: Тип действия (например, 'message', 'callback_query' и т.д.).
        - args: Аргументы, переданные вместе с действием.

        Возвращает:
        - Строку с кодом языка для текущего пользователя или его локаль по умолчанию.
        """
        
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale


def setup_lang_middleware(dp):
    
    """
    Инициализирует и регистрирует промежуточное программное обеспечение для локализации.

    Параметры:
    - dp (Dispatcher): Диспетчер Aiogram, к которому будет привязано middleware.

    Возвращает:
    - Экземпляр ACLMiddleware, используемый для локализации.
    """
    
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
