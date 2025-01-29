import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN
from recipes import get_random_recipe

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функція для створення клавіатури
def create_keyboard(name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Інша страва", callback_data="new_recipe"),
         InlineKeyboardButton(text="Рецепт", callback_data=f"recipe_{name}")]
    ])

# Обробник команди /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привіт! Я бот, який допоможе вибирати страви. Натискай /menu!")

# Обробник команди /menu
@dp.message(Command("menu"))
async def send_recipe(message: types.Message):
    name, instructions, image_url = get_random_recipe()

    if name:
        keyboard = create_keyboard(name)
        await message.answer_photo(image_url, caption=f"Страва: {name}", reply_markup=keyboard)
    else:
        await message.answer("Не вдалося отримати рецепт :( Спробуйте ще раз.")

# Обробник кнопки "Інша страва"
@dp.callback_query(lambda call: call.data == "new_recipe")
async def new_recipe(call: types.CallbackQuery):
    name, instructions, image_url = get_random_recipe()

    if name:
        keyboard = create_keyboard(name)
        await call.message.answer_photo(image_url, caption=f"Страва: {name}", reply_markup=keyboard)
    else:
        await call.message.answer("Не вдалося отримати рецепт :( Спробуйте ще раз.")

# Обробник кнопки "Рецепт"
@dp.callback_query(lambda call: call.data.startswith("recipe_"))
async def show_recipe(call: types.CallbackQuery):
    name = call.data.split("_", 1)[1]  # Отримуємо назву страви з callback_data
    _, instructions, _ = get_random_recipe()  # Тільки інструкції без зміни рецепта

    if instructions:
        await call.message.answer(f"Рецепт для {name}:\n\n{instructions}")
    else:
        await call.message.answer("Не вдалося завантажити рецепт :(")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
