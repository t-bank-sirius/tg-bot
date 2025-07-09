import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters.command import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic_settings import BaseSettings, SettingsConfigDict


dp = Dispatcher()


class BotSettings(BaseSettings):
    TOKEN: str

    model_config = SettingsConfigDict(env_prefix='BOT_')
    
    
@dp.message(CommandStart())
async def start_bot(message: Message):
    web_app = WebAppInfo(url="https://pretty-keys-battle.loca.lt/auth")
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Приложение",
        web_app=web_app)
    )

    await message.answer("Привет! Открой мини-приложение👇", reply_markup=builder.as_markup(resize_keyboard=True))


async def main():
    env = BotSettings()
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=env.TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())