from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .db import get_session
from .models import TgUser

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: Message):
    async with get_session() as s:
        user = await s.get(TgUser, msg.chat.id)
        if not user:
            s.add(
                TgUser(
                    id=msg.chat.id,
                    username=msg.from_user.username,
                    first_name=msg.from_user.first_name,
                    joined_at=datetime.utcnow(),
                )
            )
            await s.commit()
    await msg.answer("Привет! Ты сохранён в базе ✅")


@router.message(Command("ping"))
async def cmd_ping(msg: Message):
    await msg.answer("pong")