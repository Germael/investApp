from typing import Annotated

from fastapi import APIRouter, Depends
from repository.bot import Bot
from repository.info_provider import InfoProvider

info_router = APIRouter(prefix="/info")


@info_router.get("/overview")
async def get_overview(
        info_provider: Annotated[InfoProvider, Depends()],
        bot: Annotated[Bot, Depends()]
):
    message = info_provider.get_ordered_info_message("Best performers\n\n", "current_price_change")
    await bot.send_to_telegram(message)

    message = info_provider.get_ordered_info_message("Worst performers\n\n", "current_price_change", "ASC")
    await bot.send_to_telegram(message)
