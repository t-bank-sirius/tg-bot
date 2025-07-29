from aiohttp import ClientSession
from main.settings import AppSettings, JWTSecrets


async def new_message(message: str, user_id: int, image: str = None):
    app = AppSettings()
    jwt = JWTSecrets()
    
    data = {
        'telegram_id': user_id,
        'message_text': message,
        'image': image
    }
    
    headers = {
        app.HEADER_TYPE: jwt.SECRET
    }
    
    try:
        async with ClientSession() as session:
            async with session.post(f'{app.SERVER_URL}/user/new-message', json=data, headers=headers) as response:
                resp = await response.json()
                return resp
                
    except Exception:
        return {'detail': 'Извините, но нам не удалось обработать ваш текущий запрос. Пожалуйста, попробуйте ещё раз'}


async def clear_context(user_id: int):
    app = AppSettings()
    jwt = JWTSecrets()
    
    data = {
        'telegram_id': user_id
    }
    
    headers = {
        app.HEADER_TYPE: jwt.SECRET
    }
    
    try:
        async with ClientSession() as session:
            async with session.post(f'{app.SERVER_URL}/user/clear-context', json=data, headers=headers) as response:
                resp = await response.json()
                return resp
                
    except Exception:
        return {'detail': 'Извините, но нам не удалось обработать ваш текущий запрос. Пожалуйста, попробуйте ещё раз'}