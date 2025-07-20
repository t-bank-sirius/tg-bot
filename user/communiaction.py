from io import BytesIO
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, BufferedInputFile
from server_requests.requests import new_message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from .photo import decode, encode_image_from_bytesio
from telegramify_markdown import markdownify


async def convert_markdown_to_telegram(text: str) -> str:
    try:
        return markdownify(text, max_line_length=None, normalize_whitespace=False)
    except Exception:
        return text or "error"


router = Router(name=__name__)


class ChatState(StatesGroup):
    waiting = State()
    

class PhotoState(StatesGroup):
    caption = State()


async def response(message: Message, state: FSMContext, mesg: dict):
    if mesg.get('image'):
        buffer = await decode(mesg['image'])
        image_bytes = buffer.read()
        file = BufferedInputFile(image_bytes, filename="photo.jpg")

        await ChatActionSender.upload_photo(chat_id=message.chat.id, bot=message.bot)
        await message.bot.send_photo(chat_id=message.chat.id, photo=file)
        
    raw_text = mesg.get('detail') or mesg.get('message', '')
    formatted = await convert_markdown_to_telegram(raw_text)

    try:
        await message.answer(text=formatted, parse_mode='MarkdownV2')
    except Exception:
        await message.answer(text=raw_text)

    await state.clear()


async def check_or_set_wait(message: Message, state: FSMContext):
    current_state = await state.get_state()
        
    if current_state == ChatState.waiting.state:
        await message.answer(
            text='Подождите, я выполняю ваш прежний запрос...⌛'
        )
        return
        
    await state.set_state(ChatState.waiting)

    
@router.message(PhotoState.caption, F.text)
async def get_caption(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    data = await state.get_data()
    await state.clear()
    
    await summary_with_photo(message=message, state=state, **data)

        
@router.message(F.text)
async def text(message: Message, state: FSMContext):
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        await check_or_set_wait(message=message, state=state)
        mesg: str | dict = await new_message(message=message.text, user_id=message.from_user.id)
    
    await response(message=message, state=state, mesg=mesg)  


@router.message(F.photo)
async def send_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    buffer = BytesIO()
    
    await message.bot.download_file(file.file_path, destination=buffer)

    buffer.seek(0)
    b64_string = encode_image_from_bytesio(buffer)
    
    if message.caption:
        await summary_with_photo(message=message, state=state, buffered=b64_string, caption=message.caption)
    else:
        await state.update_data(buffered=b64_string)
        await state.set_state(PhotoState.caption)
        await message.answer(
            text='Что ты хочешь, чтобы я сделал с этим фото?'
        )


async def summary_with_photo(message: Message, state: FSMContext, **data):
    caption = data['caption']
    buffered = data['buffered']
    
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=message.bot):
        await check_or_set_wait(message=message, state=state)
        mesg: str | dict = await new_message(message=caption, user_id=message.from_user.id, image=buffered)
    
    await response(message=message, state=state, mesg=mesg)  
