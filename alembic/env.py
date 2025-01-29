import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Go up to the project root




# Add the project's base directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adds the parent directory (project root)

print("Python Path:", sys.path)  # Print the Python path to debug

from models.hr import User  # This should now work

from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
from models.hr import User  # Try importing here directly

# This is your metadata object
from database import Base

config = context.config
fileConfig(config.config_file_name)

# Here you configure the connection
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
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
