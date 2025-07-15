from aiogram import Router
from user.communiaction import router as communication_router


router = Router()
router.include_routers(
    communication_router
)