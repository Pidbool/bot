import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.markdown import bold

# Настройки
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  # Пример URL API Mistral.ai  (это на всякий случай "https://api.chat.mistral.ai/v1/chat")
MISTRAL_API_KEY = "4qhUbVo5GUcyxgn6foLjNR9CI8M7QdfP"  # Замени на свой API-ключ Mistral.ai
TELEGRAM_BOT_TOKEN = "7399343968:AAFOzSCksoOmC5iAQRaex3QAhdQ5q4_PE6M"  # Замени на токен своего бота

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

# Создание клавиатуры с кнопками
def create_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Новый чат"))
    builder.add(KeyboardButton(text="Профиль пользователя"))
    builder.add(KeyboardButton(text="Перезапустить бота (/start)"))
    return builder.as_markup(resize_keyboard=True)

# Функция для отправки запроса к Mistral.ai API
async def ask_mistral(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-medium",  # Укажи модель, если требуется
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        logger.error(f"Ошибка API Mistral.ai: {response.status_code}, {response.text}")
        return "Произошла ошибка при обработке запроса!"

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    welcome_message = (
        f"Привет, дорогой друг, {bold(user.first_name)} 😘! Я бот 🤖 с интеграцией одной из важнейших нейросетей современности 🧬🌐🧬.\n\n"
        "Вот что я умею 👇:\n"
        "1. Отвечаю на твои сообщения с помощью нейросети 🌐.\n"
        "2. Предоставляю информацию о твоём профиле 👤, то есть твой уникальный id 💡.\n"
        "3. Перезапускаюсь по твоей команде, если что-то пойдёт не так.\n\n"
        "Однако, если я начну тупить, то ты смело можешь нажать на кнопку 'Новый чат 💬' или 'Перезапустить бота 🔄' ! Если запрос не не обрабатывается, то проверь соединение с интернетом 🌐🛜! А может, это я такой тупой бот, что не могу обработать запрос 🥲."
        "Используй кнопки ниже, чтобы взаимодействовать со мной!"
    )
    await message.answer(welcome_message, reply_markup=create_keyboard())

# Обработка кнопки "Новый чат"
@dp.message(lambda message: message.text == "Новый чат 🎉")
async def new_chat(message: types.Message):
    await message.answer("Начинаем новый чат💬! Напиши мне что-нибудь, и я отвечу с помощью нейросети 🧬🌐🧬.")

# Обработка кнопки "Профиль пользователя"
@dp.message(lambda message: message.text == "Профиль пользователя 👤")
async def user_profile(message: types.Message):
    user = message.from_user
    profile_message = (
        f"Твой ID💡: {bold(user.id)}\n"
        "Ты самый лучший 💪! У тебя всё получится🎉! Знай это, и ты победишь 🏆!"
    )
    await message.answer(profile_message)

# Обработка кнопки "Перезапустить бота (/start)"
@dp.message(lambda message: message.text == "Перезапустить бота 🔄(/start)")
async def restart_bot(message: types.Message):
    await start(message)

# Обработка текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text
    logger.info(f"Пользователь написал: {user_message}")

    if user_message not in ["Новый чат 💬", "Профиль пользователя 👤", "Перезапустить бота 🔄(/start)"]:
        # Отправляем запрос к Mistral.ai
        response = await ask_mistral(user_message)
        await message.answer(response)

# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())