import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# -------------------------------------------------
# ADD PROJECT ROOT TO PYTHON PATH  (IMPORTANT)
# -------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Now imports will work
from app.core.config import settings
from app.models import Base

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Metadata for autogeneration
target_metadata = Base.metadata

DATABASE_URL = settings.database_url


def run_migrations_online():
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True
    )

    async def run():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run())


run_migrations_online()

