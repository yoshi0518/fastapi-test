import importlib
import os
import sys
from glob import glob
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import MetaData, engine_from_config, pool

from config import config as config_root
from db.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# alembic.iniの'sqlalchemy.url'を.envの値で書き換える
DATABASE_URL = f"postgresql+psycopg2://{config_root.neon_user}:{config_root.neon_password}@{config_root.neon_host}/{config_root.neon_db}?sslmode=require&channel_binding=require"
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# modelsディレクトリを反映
target_models = [
    os.path.splitext(os.path.basename(f))[0]
    for f in glob(str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/models/*")
    if "__init__" not in f and "__pycache__" not in f
]
sys.path.append(str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/models")


def include_name(name, type_, _):
    if type_ == "table":
        return name in target_metadata.tables
    else:
        return True


class BaseEnv:
    @staticmethod
    def make_target_metadata():
        lst = [importlib.import_module(x).Base.metadata for x in target_models]  # ty: ignore[unresolved-attribute]
        m = MetaData()
        for metadata in lst:
            for t in metadata.tables.values():
                t.tometadata(m)
        return m


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=config_root.neon_schema,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    target_metadata = BaseEnv.make_target_metadata()
    with connectable.connect() as connection:
        # DOC:
        # https://gist.github.com/utek/6163250
        # https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_name=include_name,
            include_schemas=False,
            version_table_schema=config_root.neon_schema,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
