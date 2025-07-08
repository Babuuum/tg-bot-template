from logging.config import fileConfig
import asyncio, os, sys
from pathlib import Path

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.models import *  # noqa: F401

config = context.config
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

    async with connectable.begin() as conn:

        def do_run_migrations(connection):
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()

        await conn.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
