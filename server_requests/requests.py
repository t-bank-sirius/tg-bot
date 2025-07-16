from aiohttp import ClientSession


async def new_message(message: str, user_id: int, image: str = None):
    data = {
        'telegram_id': user_id,
        'message_text': message,
        'image': image
    }
    
    try:
        async with ClientSession() as session:
            async with session.post('http://host.docker.internal:8002/user/new-message', json=data) as response:
                resp = await response.json()
                return resp
                
    except Exception as er:
        return str(er)
        return 'Возникла ошибка'