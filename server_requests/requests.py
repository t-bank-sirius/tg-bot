from aiohttp import ClientSession
from main.settings import AppSettings


async def new_message(message: str, user_id: int, image: str = None):
    app = AppSettings()
    
    data = {
        'telegram_id': user_id,
        'message_text': message,
        'image': image
    }
    
    try:
        async with ClientSession() as session:
            async with session.post(f'{app.SERVER_URL}/user/new-message', json=data) as response:
                resp = await response.json()
                return resp
                
    except Exception as er:
        return str(er)
        return 'Возникла ошибка'