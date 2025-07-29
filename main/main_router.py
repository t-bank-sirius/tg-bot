from aiogram import Router
from user.communiaction import router as communication_router
from user.context import router as context_router


router = Router()
router.include_routers(
    context_router,
    communication_router
)