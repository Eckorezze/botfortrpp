import asyncio

from aiogram import types

from keyboards import keyboards as kb
from main import dp, _, bot
from middlewares.throttling_middleware import rate_limit


@rate_limit(1)
@dp.message_handler(text=['🎮Entertainments', '🎮Развлечения'])
async def entertainments_handler(message: types.Message):
    await message.answer(_('Hi\, this is the entertainment section\!'), reply_markup=kb.return_entertainment_keyboard())


@rate_limit(4)
@dp.message_handler(
    text=["Кубик🎲", 'Dice🎲'])
async def entertainment(message: types.Message):
    result: types.Message = await bot.send_dice(message.chat.id, emoji=f'{message.text}',
                                                allow_sending_without_reply=True)
    dice_result = result.dice.value

    await asyncio.sleep(4)

    if message.text in ['Dice🎲', 'Кубик🎲']:
        await message.reply(_("The dice rolled *{dice_result}*").format(dice_result=dice_result),
                            parse_mode='Markdown')
