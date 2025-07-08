import os
import secrets
from pathlib import Path

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dotenv import load_dotenv
from sqlmodel import select
from sqlalchemy import func

from .db import get_session, init_db
from .models import TgUser
from . import handlers

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = (
    os.getenv("WEBHOOK_URL")
    or f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN')}"
)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "wh")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "adminpass")

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()
dp.include_router(handlers.router)

app = FastAPI(title="Telegram Bot via Webhook")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

security = HTTPBasic()


def check_basic(credentials: HTTPBasicCredentials = Depends(security)):
    ok_user = secrets.compare_digest(credentials.username, ADMIN_USER)
    ok_pass = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (ok_user and ok_pass):
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "Basic realm=Protected"},
        )


@app.on_event("startup")
async def on_startup():
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

@app.post(WEBHOOK_PATH, status_code=status.HTTP_200_OK, tags=["telegram"])
async def telegram_webhook(update: dict):
    await dp.feed_update(bot, Update(**update))
    return JSONResponse({"ok": True})


@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}


@app.get(
    "/admin",
    response_class=HTMLResponse,
    dependencies=[Depends(check_basic)],
    tags=["admin"],
)
async def admin(request: Request):
    async with get_session() as s:
        total_users = (
            await s.scalar(select(func.count()).select_from(TgUser))
        ) or 0
    me = await bot.get_me()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "bot_username": me.username,
            "webhook_url": f"{WEBHOOK_URL}{WEBHOOK_PATH}",
            "total_users": total_users,
        },
    )