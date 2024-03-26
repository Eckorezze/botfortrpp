import asyncio
import logging
import os
from io import BytesIO

import pandas as pd
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

import config
import keyboards as kb
from main import dp, bot, _
from messages import bot_messages as bm
from middlewares.throttling_middleware import rate_limit
from services import DataBase


storage = MemoryStorage()

db = DataBase()

admin_id = config.admin_id


@dp.message_handler(user_id=admin_id, commands=['admin'])
@rate_limit(2)
async def admin(message: types.Message):
    
    """
    Админ-панель бота. Показывает информацию для администраторов в личных сообщениях.
    Выводит количество пользователей и предоставляет интерфейс управления.

    :param message: Объект сообщения, который содержит команду.
    """
    
    await dp.bot.send_chat_action(message.chat.id, "typing")

    if message.chat.type == 'private':
        user_id = message.from_user.id

        logging.info(f"User action: /admin (User ID: {user_id})")

        user_count = await db.user_count()

        await message.answer(bm.admin_panel(
            user_count),
            reply_markup=kb.admin_keyboard(), parse_mode='MarkdownV2')
    else:
        await message.answer(bm.not_groups())


@dp.callback_query_handler(lambda call: call.data == 'send_to_all')
async def send_to_all_callback(call: types.CallbackQuery):
    
    """
    Инициирует процедуру рассылки сообщений всем пользователям. Показывает клавиатуру для ввода сообщения.

    :param call: Объект коллбэк-квери от кнопки рассылки.
    """
    
    await bot.send_message(chat_id=call.message.chat.id,
                           text=bm.mailing_message(),
                           reply_markup=kb.cancel_keyboard())
    await dp.current_state().set_state("send_to_all_message")


@dp.message_handler(state="send_to_all_message")
async def send_to_all_message(message: types.Message, state: FSMContext):
    
    """
    Отправляет введённое администратором сообщение всем пользователям бота.

    :param message: Сообщение от администратора, которое нужно рассылать.
    :param state: Текущее состояние FSM.
    """
    
    sender_id = message.from_user.id
    if message.text == _("↩️Cancel"):
        await bot.send_message(message.chat.id, bm.canceled(), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    else:
        await dp.bot.send_chat_action(message.chat.id, "typing")

        users = await db.all_users()

        for user in users:
            try:
                await bot.copy_message(chat_id=user[0],
                                       from_chat_id=sender_id,
                                       message_id=message.message_id,
                                       parse_mode="MarkdownV2")
                logging.info(f"Sent message to user {user[0]}: {message.text}")
            except Exception as e:
                logging.error(
                    f"Error sending message to user {user[0]}: {str(e)}")
                continue
        await bot.send_message(chat_id=message.chat.id,
                               text=bm.finish_mailing(), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return


@dp.callback_query_handler(lambda call: call.data == 'control_user')
async def control_user_callback(call: types.CallbackQuery):
    
    """
    Обработчик команды управления пользователями. Позволяет администратору искать пользователей
    по различным критериям и управлять ими.

    :param call: Объект коллбэк-квери от кнопки управления пользователями.
    """
    
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text=_('Search user by:'), reply_markup=kb.return_search_keyboard())


@dp.callback_query_handler(lambda call: call.data.startswith("search_"))
async def search_user_by(call: types.CallbackQuery):
    
    search = call.data.split('_')[1]
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text=_('Type user {search}:').format(search=search), reply_markup=kb.cancel_keyboard())

    await dp.current_state().set_state("control_user")
    await dp.current_state().update_data(search=search)


@dp.message_handler(state="control_user")
async def control_user(message: types.Message, state: FSMContext):
    
    """
    Позволяет администратору управлять найденным пользователем: блокировать, разблокировать,
    просматривать информацию.

    :param message: Сообщение, в котором указано действие над пользователем.
    :param state: Текущее состояние FSM.
    """
    
    answer = message.text
    answer = answer.replace("@", "")
    answer = answer.replace("https://t.me/", "")
    data = await state.get_data()
    search = data.get("search")

    if message.text == _("↩️Cancel"):
        await bot.send_message(message.chat.id,
                               'Action canceled\!',
                               reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await admin(message)
        return

    else:
        await dp.bot.send_chat_action(message.chat.id, "typing")

        clock = await bot.send_message(message.chat.id, '⏳', reply_markup=ReplyKeyboardRemove())

        await asyncio.sleep(2)

        await bot.delete_message(message.chat.id, clock.message_id)

        user = None

        if search == "id":
            user = await db.get_user_info(answer)

        elif search == "username":
            user = await db.get_user_info_username(answer)

        result = user.fetchone()

        if result is not None:
            user_name = None
            user_username = None
            status = None
            user_id = None

            if search == "id":
                user_name, user_username, status = result
                user_id = answer

            elif search == "username":
                user_name, user_id, status = result
                user_username = answer

            go_to_chat = InlineKeyboardButton(text=_("Enter in Conversation"), url=f"tg://user?id={user_id}")
            write_user = InlineKeyboardButton(text=_('Write as a bot'), callback_data=f"write_{user_id}")
            ban_button = InlineKeyboardButton(text=_("❌Ban"), callback_data=f"ban_{user_id}")
            unban_button = InlineKeyboardButton(text=_("✅Unban"), callback_data=f"unban_{user_id}")
            back_button = InlineKeyboardButton(text=_("🔙Back"), callback_data="back_to_admin")
            control_keyboard = InlineKeyboardMarkup()
            control_keyboard.row(go_to_chat, write_user)

            if user_username == "":
                user_username = "None"
            else:
                user_username = f"@{user_username}"

            user_photo = await bot.get_user_profile_photos(user_id, limit=1)

            if status == 'user':
                control_keyboard.row(ban_button)

            elif status == 'ban':
                control_keyboard.row(unban_button)

            control_keyboard.row(back_button)

            if user_photo.total_count > 0:
                await message.reply_photo(user_photo.photos[0][-1].file_id,
                                          caption=bm.return_user_info(user_name, user_id, user_username, status),
                                          reply_markup=control_keyboard, parse_mode="MarkdownV2")
            else:
                await bot.send_message(message.chat.id, bm.return_user_info(user_name, user_id, user_username, status),
                                       reply_markup=control_keyboard, parse_mode="MarkdownV2")
            logging.info(f"Control user: {user_id}")

        else:
            await bot.send_message(message.chat.id, _("User not found\!"))

        await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith("ban_"))
async def message_handler(call: types.CallbackQuery):
    
    """
    Обрабатывает запрос на блокировку пользователя. Запрашивает у администратора причину блокировки.

    :param call: Коллбэк-квери, содержащее информацию для блокировки пользователя.
    """
    
    banned_user_id = call.data.split("_")[1]

    await call.message.delete()
    await call.message.answer(_('Enter ban reason:'), reply_markup=kb.cancel_keyboard())
    await dp.current_state().set_state("ban_reason")
    await dp.current_state().update_data(banned_user_id=banned_user_id)


@dp.message_handler(state="ban_reason")
async def control_user(message: types.Message, state: FSMContext):
    
    """
    Получает и обрабатывает причину блокировки пользователя. Выполняет блокировку.

    :param message: Сообщение, содержащее причину блокировки.
    :param state: Текущее состояние FSM.
    """
    
    reason = message.text
    data = await state.get_data()
    banned_user_id = data.get("banned_user_id")

    if message.text == _("↩️Cancel"):
        await bot.send_message(message.chat.id, _('Action canceled\!'),
                               reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await admin(message)
        return

    await db.ban_user(banned_user_id)

    await state.finish()

    await bot.send_message(chat_id=banned_user_id,
                           text=bm.ban_message(reason),
                           reply_markup=ReplyKeyboardRemove())

    ban_message = await message.answer(bm.successful_ban(banned_user_id),
                                       reply_markup=ReplyKeyboardRemove())

    await bot.delete_message(message.chat.id, ban_message.message_id)

    await message.answer(bm.successful_ban(banned_user_id), reply_markup=kb.return_back_to_admin_keyboard())

    logging.info(f"Banned user: {banned_user_id} Reason: {reason}")


@dp.callback_query_handler(lambda call: call.data.startswith("unban_"))
async def message_handler(call: types.CallbackQuery):
    
    """
    Обрабатывает запрос на разблокировку пользователя.

    :param call: Коллбэк-квери, содержащее информацию для разблокировки пользователя.
    """
    
    unbanned_user_id = call.data.split("_")[1]

    await db.unban_user(unbanned_user_id)

    await bot.send_message(chat_id=unbanned_user_id,
                           text=bm.unban_message())

    await call.message.delete()

    await call.message.answer(bm.successful_unban(unbanned_user_id),
                              reply_markup=kb.return_back_to_admin_keyboard())

    logging.info(f"Unbanned user: {unbanned_user_id}")


@dp.message_handler(user_id=admin_id, commands=['get_users'])
async def export_users_data(message: types.Message):
    
    """
    Экспортирует данные всех пользователей в Excel файл и отправляет его администратору.

    :param message: Сообщение, инициирующее экспорт данных.
    """
    
    clock = await bot.send_message(message.chat.id, '⏳', reply_markup=ReplyKeyboardRemove())
    users = await db.all_users()

    for user in users:
        chat_id = user[0]

        try:
            user = await bot.get_chat(chat_id)
        except Exception as e:
            if str(e) == 'Chat not found':
                await db.delete_user(chat_id)

            print(f"An error occurred: {str(e)} Chat ID: {chat_id}")
            continue

        username = user.username if user.username else ""
        full_name = user.full_name if user.full_name else ""
        await db.user_update_name(chat_id, full_name, username)

    await asyncio.sleep(2)

    users_data = await db.get_all_users_info()

    df = pd.DataFrame(users_data, columns=['user_id', 'user_name', 'user_username', 'language', 'status'])

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)

    file_path = 'users_data.xlsx'
    with open(file_path, 'wb') as file:
        file.write(excel_file.getvalue())

    await bot.delete_message(message.chat.id, clock.message_id)

    with open(file_path, 'rb') as file:
        await bot.send_document(chat_id=message.chat.id, document=file)

    logging.info(f"Getting info about user")

    os.remove(file_path)


@dp.callback_query_handler(lambda call: call.data == 'back_to_admin')
async def back_to_admin(call: types.CallbackQuery):
    
    """
    Возвращает администратора к админ-панели.

    :param call: Коллбэк-квери, сигнализирующее о возвращении.
    """
    
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_chat_action(call.message.chat.id, "typing")

    user_count = await db.user_count()

    await call.message.answer(bm.admin_panel(user_count),
                              reply_markup=kb.admin_keyboard(),
                              parse_mode='MarkdownV2')


@dp.callback_query_handler(lambda call: call.data.startswith("answer_"))
async def answer_feedback_handler(call: types.CallbackQuery):
    
    """
    Позволяет администратору ответить на сообщение пользователя.

    :param call: Коллбэк-квери, содержащее запрос на ответ.
    """
    
    message_id = call.data.split("_")[1]
    chat_id = call.data.split("_")[2]
    await call.message.delete_reply_markup()
    await call.message.answer(_('Please type your answer:'), reply_markup=kb.cancel_keyboard())
    await dp.current_state().set_state('feedback_answer')
    await dp.current_state().update_data(message_id=message_id, chat_id=chat_id)


@dp.message_handler(state='feedback_answer')
async def answer_feedback(message: types.Message, state: FSMContext):
    
    """
    Обрабатывает и отправляет ответ администратора на сообщение пользователя.

    :param message: Сообщение с ответом.
    :param state: Текущее состояние FSM.
    """
    
    answer = message.text

    if answer == _("↩️Cancel"):
        await bot.send_message(message.chat.id, _('Action canceled\!'), reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    data = await state.get_data()
    message_id = data.get('message_id')
    chat_id = data.get('chat_id')
    await state.finish()

    try:
        await bot.send_message(chat_id=chat_id,
                               text=_('Your message *{message_id}* was seen\!\n*Answer:* `{answer}`').format(
                                   message_id=message_id, answer=answer))
        await message.reply(_('Your answer sent\!'), reply_markup=ReplyKeyboardRemove())
        logging.info(f"Sent answer for feedback to user {chat_id}: {answer}")

    except Exception as e:
        await message.reply(_("Something went wrong, see log for more information\!"),
                            reply_markup=kb.return_back_to_admin_keyboard())
        logging.error(f"Error sending message to user {chat_id}: {str(e)}")


@dp.callback_query_handler(lambda call: call.data.startswith("write_"))
async def write_message_handler(call: types.CallbackQuery):
    
    """
    Позволяет администратору написать сообщение от имени бота.

    :param call: Коллбэк-квери, содержащее запрос на написание сообщения.
    """
    
    chat_id = call.data.split("_")[1]
    await call.message.delete_reply_markup()
    await call.message.delete()
    await call.message.answer(_('Please type message:'), reply_markup=kb.cancel_keyboard())
    await dp.current_state().set_state('write_message')
    await dp.current_state().update_data(chat_id=chat_id)


@dp.message_handler(state='write_message')
async def write_message(message: types.Message, state: FSMContext):
    
    """
    Отправляет сообщение от имени бота в чат пользователя.

    :param message: Сообщение для отправки.
    :param state: Текущее состояние FSM.
    """
    
    answer = message.text

    if answer == _("↩️Cancel"):
        await bot.send_message(message.chat.id, _('Action canceled\!'), reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    data = await state.get_data()
    chat_id = data.get('chat_id')
    await state.finish()

    try:
        await bot.send_message(chat_id=chat_id,
                               text=answer)
        message_sent = await message.reply(_('Your message sent\!'), reply_markup=ReplyKeyboardRemove())

        await bot.delete_message(message.chat.id, message_sent.message_id)

        await message.answer(_('Your message sent\!'), reply_markup=kb.return_back_to_admin_keyboard())

        logging.info(f"Sent message as bot to user {chat_id}: {answer}")

    except Exception as e:
        await message.reply(_("Something went wrong, see log for more information\!"),
                            reply_markup=kb.return_back_to_admin_keyboard())
        logging.error(f"Error sending message to user {chat_id}: {str(e)}")