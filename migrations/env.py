import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import DATABASE_URL
from app.db.models import Base

# this is the Alembic Config object, which provides access to the .ini file values
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# set the target metadata for 'autogenerate' support
target_metadata = Base.metadata

config.set_main_option('sqlalchemy.url', DATABASE_URL)


async def run_migrations_online():
    """Run migrations in 'online' mode using async connection."""

    # Create an AsyncEngine for async migrations
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Helper to run migrations in sync context."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# This is the async entry point for running migrations
asyncio.run(run_migrations_online())
