from aiogram import Router, F
from aiogram.types import Message
from server_requests.requests import clear_context


router = Router(name=__name__)


@router.message(F.text == 'Очистить контекст')
async def context_clear(message: Message):
    context = await clear_context(message.from_user.id)
    
    if context.get('detail'):
        await message.answer(text=context['detail'])
    else:
        await message.answer(text='Контекст с текущим персонажем был успешно очищен')