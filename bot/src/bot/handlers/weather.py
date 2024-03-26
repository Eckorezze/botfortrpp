import asyncio
import datetime
import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers import users as hu
import keyboards as kb
from main import dp, bot, _
from middlewares.throttling_middleware import rate_limit
from services import DataBase

WEATHER_API_KEY = "5a790b0dd84fd7bf42f2b82544390aa9"

db = DataBase()


class Weather(StatesGroup):
    
    """
    Определяет состояния для получения погоды или прогноза.

    Состояния:
    - get_location: Состояние для получения местоположения пользователя.
    - weather_or_forecast: Состояние для выбора между текущей погодой и прогнозом.
    """
    
    get_location = State()
    weather_or_forecast = State()


@rate_limit(1)
@dp.message_handler(text=["🌦Weather", "🌦Погода"])
async def get_url_type(message: types.Message):
    
    """
    Запрашивает местоположение пользователя для предоставления погоды.

    Аргументы:
    - message (types.Message): Сообщение от пользователя.
    """
    
    await message.answer(_("Please share your location"), reply_markup=kb.return_location_keyboard())


@rate_limit(1)
@dp.message_handler(content_types=['location'])
async def send_location(message: types.Message, state: FSMContext):
    
    """
    Обрабатывает получение местоположения от пользователя.

    Аргументы:
    - message (types.Message): Сообщение от пользователя с местоположением.
    - state (FSMContext): Контекст состояния для хранения информации между шагами.
    """
    
    message_str = message.location
    print(message_str)

    await message.answer(_("What do you want to get?"), reply_markup=kb.return_weather_or_forecast_keyboard())
    await Weather.weather_or_forecast.set()
    await state.update_data(location=message_str)


@dp.message_handler(state=Weather.weather_or_forecast)
async def send_weather(message: types.Message, state: FSMContext):
    
    """
    Обрабатывает выбор пользователя между получением текущей погоды или прогноза.

    Использует OpenWeatherMap API для получения данных и отправляет их пользователю.

    Аргументы:
    - message (types.Message): Сообщение от пользователя с выбором типа погоды.
    - state (FSMContext): Контекст состояния с сохраненным местоположением пользователя.
    """
    
    if message.text == _('📂Menu'):
        await hu.send_welcome(message)
        await state.finish()
        return

    user_id = message.from_user.id
    language = await db.get_language(user_id)
    data = await state.get_data()
    location = data["location"]

    wait_message = await bot.send_message(message.chat.id, "⏳", reply_markup=types.ReplyKeyboardRemove())

    await asyncio.sleep(1)

    if message.text == _('Current weather'):
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&lang={language}&appid=%s' % (
                location.latitude, location.longitude, WEATHER_API_KEY))
        if response.status_code == 200:
            weather_data = response.content
            weather_data = json.loads(weather_data.decode('utf-8'))
            temperature = round(float(weather_data['main']['temp']) - 273.15, 3)
            await bot.send_message(message.chat.id,
                                   _('<b>Location: %s</b>\nWeather: %s\nWeather description: %s\nTemperature: %s°C') % (
                                       weather_data['name'], weather_data['weather'][0]['main'],
                                       weather_data['weather'][0]['description'], temperature), parse_mode='html',
                                   reply_markup=kb.return_select_keyboard())
        else:
            await bot.send_message(message.chat.id, _('Something went wrong, try again, please'),
                                   reply_markup=kb.return_select_keyboard())

    elif message.text == _('Forecast for tomorrow'):
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?lat=%f&lon=%f&cnt=10&lang={language}&appid=%s' % (
                location.latitude, location.longitude, WEATHER_API_KEY))
        if response.status_code == 200:
            weather_data = response.content
            weather_data = json.loads(weather_data.decode('utf-8'))
            weather_data['list'] = weather_data['list'][len(weather_data['list']) - 1]
            temperature = round(float(weather_data['list']['main']['temp']) - 273.15, 3)
            weather = weather_data['list']['weather'][0]['main']
            weather_description = weather_data['list']['weather'][0]['description']
            location = weather_data['city']['name'] + ' ' + weather_data['city']['country']
            forecast_time = datetime.datetime.strptime(weather_data['list']['dt_txt'][0:10], '%Y-%m-%d').strftime(
                '%d-%m-%Y') + weather_data['list']['dt_txt'][10:]
            await bot.send_message(message.chat.id,
                                   _('<b>Forecast for %s</b>\n<i>Location: %s</i>\nWeather: %s\nWeather Description: '
                                     '%s\nTemperature: %s°C') % (
                                       forecast_time, location, weather, weather_description, temperature),
                                   parse_mode='html', reply_markup=kb.return_select_keyboard())
        else:
            print(response.status_code)
            await bot.send_message(message.chat.id, _('Something went wrong, try again, please'),
                                   reply_markup=kb.return_select_keyboard())
    await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)

    await state.finish()