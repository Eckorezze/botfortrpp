import logging
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
from middlewares import setup_lang_middleware, setup_ban_middlewares, setup_throttling_middlewares
from services import DataBase

# Настройка логгирования для отслеживания информации о работе бота.
logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").disabled = True

# Основные настройки бота: токен и формат сообщений.
parse_mode = "MarkdownV2"
bot = Bot(token=config.token, parse_mode=parse_mode)

# Инициализация хранилища состояний и диспетчера.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Настройка мидлварей для обработки языков, банов и ограничения частоты запросов.
i18n = setup_lang_middleware(dp)
_ = i18n.gettext
db = DataBase()


async def on_shutdown(dp):
    
    """
    Вызывается при остановке бота. Оповещает администратора о остановке.

    :param dp: Dispatcher - диспетчер бота.
    """
    
    await bot.send_message(config.admin_id, _("I'm stopped"))

async def on_startup(dp):
    
    """
    Вызывается при запуске бота. Оповещает администратора о запуске и проверяет количество пользователей.

    :param dp: Dispatcher - диспетчер бота.
    """
    
    await bot.send_message(config.admin_id, _("I'm launched"))
    await db.user_count()


async def update_info(message: types.Message):
    
    """
    Обновляет информацию о пользователе в базе данных при каждом сообщении.

    :param message: Message - сообщение от пользователя, содержащее его данные.
    """
    
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = message.from_user.username
    result = await db.user_exist(user_id)
    if result:
        await db.user_update_name(user_id, user_name, user_username)
    else:
        await db.add_users(user_id, user_name, user_username)
        

if __name__ == '__main__':
    # Импорт обработчиков для разных категорий команд.
    from handlers.admin import dp
    from handlers.users import dp
    from handlers.qr_code import dp
    from handlers.weather import dp
    from handlers.random_gen import dp
    from handlers.tasks import dp
    from handlers.entertaiment import dp
    
    # Настройка и запуск бота.
    setup_throttling_middlewares(dp)
    setup_ban_middlewares(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)