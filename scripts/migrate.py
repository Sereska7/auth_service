import asyncio
from argparse import ArgumentParser
from alembic import command
from alembic.config import Config

from app.pkg.settings import settings


def get_alembic_config(testing=False):
    alembic_cfg = Config("alembic.ini")  # путь к твоему alembic.ini
    if testing:
        alembic_cfg.set_main_option("sqlalchemy.url", settings.POSTGRES.TEST_DSN)
    else:
        alembic_cfg.set_main_option("sqlalchemy.url", settings.POSTGRES.DSN)
    return alembic_cfg


def _apply(testing=False):
    alembic_cfg = get_alembic_config(testing)
    command.upgrade(alembic_cfg, "head")


def _rollback(testing=False):
    alembic_cfg = get_alembic_config(testing)
    command.downgrade(alembic_cfg, "base")


def _rollback_one(testing=False):
    alembic_cfg = get_alembic_config(testing)
    # Откат на одну ревизию назад
    command.downgrade(alembic_cfg, "-1")


def _reload(testing=False):
    alembic_cfg = get_alembic_config(testing)
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")


async def inserter():
    """Функция для вставки тестовых данных (при необходимости)."""
    ...


def run(action, testing=False):
    action(testing)


def parse_cli_args():
    parser = ArgumentParser(description="Manage alembic migrations")
    parser.add_argument("--rollback", action="store_true", help="Rollback all migrations")
    parser.add_argument("--rollback-one", action="store_true", help="Rollback one migration")
    parser.add_argument("--reload", action="store_true", help="Rollback all and reapply")
    parser.add_argument("--testing", action="store_true", help="Use testing database")
    args = parser.parse_args()
    return args


def cli():
    args = parse_cli_args()

    if args.rollback:
        action = _rollback
    elif args.rollback_one:
        action = _rollback_one
    elif args.reload:
        action = _reload
    else:
        action = _apply

    run(action, testing=args.testing)

    if args.testing:
        run(action, testing=True)

    if not (args.rollback or args.rollback_one):
        asyncio.run(inserter())


if __name__ == "__main__":
    cli()
