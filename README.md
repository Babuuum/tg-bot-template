# Telegram Bot Template → Railway ☁️🚀  
**aiogram 3 + FastAPI + SQLModel**

---

## 🔘 Быстрый деплой

1. **Authorize GitHub** – Railway увидит репозиторий и начнёт билд по `Dockerfile`.

2. **Variables**

   | KEY (обязательно) | Пример               | Описание              |
   |-------------------|----------------------|-----------------------|
   | `BOT_TOKEN`       | `123456:ABC...`      | токен Telegram-бота   |
   | `WEBHOOK_SECRET`  | `fc65a2ce2cfdae0f`   | суффикс к `/webhook/` |
   | *(опц.)* `ADMIN_USER` | `admin`          | логин Basic-auth      |
   | *(опц.)* `ADMIN_PASS` | `changeme`       | пароль Basic-auth     |

3. **Deploy** → через 1-2 минуты бот в сети. Railway сам выдаст домен
   (`RAILWAY_PUBLIC_DOMAIN`); код подставит его в webhook автоматически.

---

## ✅ Проверка после билда

| Проверка        | URL / команда                                                          | Ожидаемый ответ                          |
|-----------------|------------------------------------------------------------------------|------------------------------------------|
| health-probe    | `GET /health`                                                         | `{"status":"ok"}`                        |
| админка         | `GET /admin` → Basic-auth                                             | страница со счётчиком пользователей      |
| бот-команда     | `/ping` в чате                                                        | `pong`                                   |
| webhook info    | `GET https://api.telegram.org/bot<TOKEN>/getWebhookInfo`              | `url` совпадает с доменом Railway        |

---

## 🔄 Миграции (если меняете модели)

```bash
# открываем Railway → Terminal
alembic revision --autogenerate -m "add field"
alembic upgrade head
