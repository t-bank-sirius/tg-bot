import logging
import asyncio

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from aiogram import Dispatcher, Bot
from aiogram.filters.command import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic_settings import BaseSettings, SettingsConfigDict


app = FastAPI()
dp = Dispatcher()
bot = None


class ServerData(BaseModel):
    chat_id: int
    init_message: str


class BotSettings(BaseSettings):
    TOKEN: str
    model_config = SettingsConfigDict(env_prefix='BOT_')


@app.post('/hello')
async def send_hello(from_server: ServerData):
    chat_id = from_server.chat_id
    text = from_server.init_message
    
    await bot.send_message(chat_id=chat_id, text=text)


@dp.message(CommandStart())
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Открыть Mini App",
        web_app=WebAppInfo(url="https://user365944644-cvuxdunx.tunnel.vk-apps.com/auth")
    ))
    await message.answer("Привет!", reply_markup=builder.as_markup())


@app.on_event("startup")
async def on_startup():
    global bot
    
    settings = BotSettings()
    bot = Bot(token=settings.TOKEN)
    
    asyncio.create_task(dp.start_polling(bot))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)