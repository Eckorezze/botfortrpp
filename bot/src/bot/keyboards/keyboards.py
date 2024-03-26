from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from main import _

lang_keyboard = InlineKeyboardMarkup()
"""
    Создаёт и возвращает клавиатуру для выбора языка.
    
    Возвращает:
    InlineKeyboardMarkup с кнопками для выбора языка.
"""
lang_keyboard.add(InlineKeyboardButton(text="Русский🇷🇺", callback_data="lang_ru"),
                  InlineKeyboardButton(text="English🇬🇧", callback_data="lang_en"))


def return_qr_type_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для выбора типа QR-кода.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопками для выбора типа QR-кода и кнопкой возврата в меню.
    """
    
    qr_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    simple_qr_button = types.KeyboardButton(_("Simple QR code"))
    wifi_qr_button = types.KeyboardButton(_("Wi-Fi QR-code"))
    menu_button = types.KeyboardButton(_('📂Menu'))
    qr_type_keyboard.row(simple_qr_button, wifi_qr_button)
    qr_type_keyboard.row(menu_button)
    return qr_type_keyboard


def return_select_keyboard():
    
    """
    Создаёт и возвращает главную клавиатуру бота с основными функциями.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопками основных функций бота.
    """
    
    select_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    qr_button = KeyboardButton(text=_("QR code"))
    wt_button = KeyboardButton(text=_("🌦Weather"))
    nt_button = KeyboardButton(text=_("🎯Tasks"))
    pass_button = KeyboardButton(text=_("🔐Generate password"))
    random_num_button = KeyboardButton(text=_("🔢Random number"))
    entertainment_button = KeyboardButton(text=_('🎮Entertainments'))
    info_button = KeyboardButton(text=_("ℹ️INFO"))
    select_keyboard.row(qr_button, wt_button, nt_button)
    select_keyboard.row(pass_button, random_num_button)
    select_keyboard.row(entertainment_button)
    select_keyboard.row(info_button)
    return select_keyboard


def return_color_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для выбора цвета.
    
    Возвращает:
    InlineKeyboardMarkup с кнопками различных цветов.
    """
    
    color_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    red_button = types.InlineKeyboardButton(text="🟥", callback_data="color_red")
    orange_button = types.InlineKeyboardButton(text="🟧", callback_data="color_orange")
    yellow_button = types.InlineKeyboardButton(text="🟨", callback_data="color_yellow")
    green_button = types.InlineKeyboardButton(text="🟩", callback_data="color_green")
    blue_button = types.InlineKeyboardButton(text="🟦", callback_data="color_blue")
    purple_button = types.InlineKeyboardButton(text="🟪", callback_data="color_purple")
    black_button = types.InlineKeyboardButton(text="⬛️", callback_data="color_black")
    white_button = types.InlineKeyboardButton(text="⬜️", callback_data="color_white")
    brown_button = types.InlineKeyboardButton(text="🟫", callback_data="color_brown")
    color_keyboard.row(red_button, orange_button, yellow_button)
    color_keyboard.row(green_button, blue_button, purple_button)
    color_keyboard.row(black_button, white_button, brown_button)
    return color_keyboard


def return_location_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для отправки геолокации.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопкой для отправки геолокации и кнопкой возврата в меню.
    """
    
    location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    send_location_button = types.KeyboardButton(_('📍Set your location'), request_location=True)
    menu_button = types.KeyboardButton(_('📂Menu'))
    location_keyboard.add(send_location_button)
    location_keyboard.add(menu_button)
    return location_keyboard


def return_weather_or_forecast_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для выбора между текущей погодой и прогнозом на завтра.
    
    Возвращает:
    ReplyKeyboardMarkup с соответствующими кнопками выбора и кнопкой возврата в меню.
    """
    
    weather_or_forecast_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    get_weather_button = types.KeyboardButton(_('Current weather'))
    get_forecast_button = types.KeyboardButton(_('Forecast for tomorrow'))
    menu_button = types.KeyboardButton(_('📂Menu'))
    weather_or_forecast_keyboard.add(get_weather_button, get_forecast_button)
    weather_or_forecast_keyboard.add(menu_button)
    return weather_or_forecast_keyboard


def return_numbers_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для выбора диапазона чисел.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопками различных числовых диапазонов.
    """
    
    numbers_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    z_h_button = types.KeyboardButton('0-99')
    z_t_button = types.KeyboardButton('0-999')
    z_tt_button = types.KeyboardButton('0-9999')
    z_ht_button = types.KeyboardButton('0-99999')
    z_m_button = types.KeyboardButton('0-999999')
    menu_button = types.KeyboardButton(_('📂Menu'))
    numbers_keyboard.row(z_h_button, z_t_button, z_tt_button)
    numbers_keyboard.row(z_ht_button, z_m_button)
    numbers_keyboard.row(menu_button)
    return numbers_keyboard


def return_menu_keyboard():
    
    """
    Создаёт и возвращает клавиатуру с кнопкой возврата в меню.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопкой возврата в меню.
    """
    
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(_('📂Menu'))
    menu_keyboard.add(menu_button)
    return menu_keyboard


def return_entertainment_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для развлечений.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопками доступных развлечений.
    """
    
    entertainment_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dice_button = types.KeyboardButton(_('Dice🎲'))
    menu_button = types.KeyboardButton(_('📂Menu'))
    entertainment_keyboard.add(dice_button)
    entertainment_keyboard.add(menu_button)
    return entertainment_keyboard


def cancel_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для отмены текущего действия.
    
    Возвращает:
    ReplyKeyboardMarkup с кнопкой отмены.
    """
    
    cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cancel = KeyboardButton(_("↩️Cancel"))
    cancel_keyboard.add(cancel)
    return cancel_keyboard


def admin_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для администратора.
    
    Возвращает:
    InlineKeyboardMarkup с кнопками управления для администратора.
    """
    
    admin_keyboard = InlineKeyboardMarkup()
    send_to_all_button = InlineKeyboardButton(
        text=_('💬Mailing'), callback_data='send_to_all')
    control_user_button = InlineKeyboardButton(text=_("👤Control User"),
                                               callback_data='control_user')

    admin_keyboard.row(send_to_all_button)
    admin_keyboard.row(control_user_button)
    return admin_keyboard


def return_search_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для поиска пользователей.
    
    Возвращает:
    InlineKeyboardMarkup с кнопками выбора критериев поиска.
    """
    
    search_keyboard = InlineKeyboardMarkup()
    id_button = InlineKeyboardButton(text="ID", callback_data="search_id")
    username_button = InlineKeyboardButton(text="Username", callback_data="search_username")
    search_keyboard.row(username_button, id_button)
    return search_keyboard


def return_back_to_admin_keyboard():
    
    """
    Создаёт и возвращает клавиатуру для возвращения в админское меню.
    
    Возвращает:
    InlineKeyboardMarkup с кнопкой возврата.
    """
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    back_button = InlineKeyboardButton(text=_("🔙Back"), callback_data="back_to_admin")
    keyboard.row(back_button)
    return keyboard


def return_feedback_button():
    
    """
    Создаёт и возвращает клавиатуру для отправки обратной связи.
    
    Возвращает:
    InlineKeyboardMarkup с кнопкой для отправки обратной связи.
    """
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    feedback_button = InlineKeyboardButton(text=_("Feedback💬"), callback_data='feedback')
    keyboard.row(feedback_button)
    return keyboard


def feedback_answer(feedback_message_id, feedback_message_chat_id):
    
    """
    Создаёт и возвращает клавиатуру для ответа на обратную связь.
    
    Аргументы:
    - feedback_message_id: Идентификатор сообщения обратной связи.
    - feedback_message_chat_id: Идентификатор чата, из которого была отправлена обратная связь.
    
    Возвращает:
    InlineKeyboardMarkup с кнопкой для ответа на обратную связь.
    """
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    answer_button = InlineKeyboardButton(text=_("Answer💬"),
                                         callback_data=f'answer_{feedback_message_id}_{feedback_message_chat_id}')
    keyboard.row(answer_button)
    return keyboard