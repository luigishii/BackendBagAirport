from __future__ import with_statement
import logging
import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
from src.database import Base  # Importa a Base de seus modelos
from src.models import User

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL do banco de dados do arquivo .env
database_url = os.getenv("DATABASE_URL")


if not database_url:
    raise ValueError("DATABASE_URL not found in .env file")

# Configura o logger
logger = logging.getLogger('alembic.env')
logger.setLevel(logging.INFO)

# Obtém a configuração do Alembic
config = context.config

config.set_main_option('sqlalchemy.url', database_url)

# Define o metadata para o Alembic usar
target_metadata = Base.metadata

def run_migrations_offline():
    """Executa migrações no modo offline."""
    context.configure(url=database_url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
