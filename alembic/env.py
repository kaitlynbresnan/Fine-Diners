from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# Alembic Config object
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load DB URI from environment and override config
def get_url():
    url = os.getenv("POSTGRES_URI") or os.getenv("postgres_uri")
    
    if not url:
        raise ValueError("Database URI not found! Check Render Environment Variable names.")

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url.replace("%", "%%")

# Import your metadata (for `--autogenerate`)
# from app.db import Base
target_metadata = None  # or Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import URL
    
    cmd_url = URL.create(
        drivername="postgresql+psycopg",
        username="postgres.sqpjgfakuiaeztzpoizd",
        password="finediners",
        host="aws-1-us-west-2.pooler.supabase.com",
        port=5432,
        database="postgresfd",
    )

    # 2. Create the engine using this object, NOT a string from os.getenv
    connectable = create_engine(
        cmd_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


# Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
