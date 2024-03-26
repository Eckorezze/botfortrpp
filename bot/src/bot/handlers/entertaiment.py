import asyncio

from aiogram import types

import keyboards as kb
from main import dp, _, bot
from middlewares.throttling_middleware import rate_limit


@rate_limit(1)
@dp.message_handler(text=['🎮Entertainments', '🎮Развлечения'])
async def entertainments_handler(message: types.Message):
    
    """
    Обрабатывает сообщения, связанные с разделом развлечений в Telegram-боте.

    Отвечает на сообщения с текстом "🎮Entertainments" или "🎮Развлечения",
    отправляя приветственное сообщение и клавиатуру развлечений.

    Args:
        message (aiogram.types.Message): Сообщение от пользователя.
    """
    
    await message.answer(_('Hi\, this is the entertainment section\!'), reply_markup=kb.return_entertainment_keyboard())


@rate_limit(4)
@dp.message_handler(
    text=["Кубик🎲", 'Dice🎲'])
async def entertainment(message: types.Message):
    
    """
    Обрабатывает команды для броска кубика в Telegram-боте.

    Поддерживает команды "Кубик🎲" и "Dice🎲", позволяя пользователю бросить кубик.
    После броска кубика бот ждет 4 секунды, прежде чем отправить результат броска.

    Args:
        message (aiogram.types.Message): Сообщение от пользователя.
    """
    
    result: types.Message = await bot.send_dice(message.chat.id, emoji=f'{message.text}',
                                                allow_sending_without_reply=True)
    dice_result = result.dice.value

    await asyncio.sleep(4)

    if message.text in ['Dice🎲', 'Кубик🎲']:
        await message.reply(_("The dice rolled *{dice_result}*").format(dice_result=dice_result),
                            parse_mode='MarkdownV2')
