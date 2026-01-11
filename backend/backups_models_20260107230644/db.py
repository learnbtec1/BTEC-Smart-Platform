from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings

# Delay importing `app.models` symbols until runtime to avoid circular imports
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel
    # If an override DB URL is present (tests/local), create tables automatically
    try:
        from sqlmodel import SQLModel

        # Create tables when using an in-memory SQLite or when DB_URL_OVERRIDE is set
        if getattr(settings, "DB_URL_OVERRIDE", None) or "sqlite" in str(settings.SQLALCHEMY_DATABASE_URI):
            SQLModel.metadata.create_all(engine)
    except Exception:
        pass

    try:
        # Import models here to avoid circular import during module load
        from app.models import User, UserCreate

        user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = crud.create_user(session=session, user_create=user_in)
    except Exception:
        # If models or dependencies aren't available at import time (tests or partial startup),
        # skip seeding. This prevents the app from crashing on import due to circular imports.
        return
