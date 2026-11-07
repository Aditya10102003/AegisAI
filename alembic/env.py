import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.core.config import settings
from app.models.base import Base
from app.models import (
    department,
    employee,
    role,
    permission,
    resource,
    access_request,
    access_grant,
    audit_log,
    user_role,
    role_permission,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from alembic import context

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Set the database URL from the settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
print("DATABASE_URL =", settings.DATABASE_URL)
print("ALEMBIC_URL =", config.get_main_option("sqlalchemy.url"))

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()