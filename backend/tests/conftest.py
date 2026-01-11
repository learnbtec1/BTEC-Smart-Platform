from collections.abc import Generator
import sys
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
import os

# Ensure pytest imports the correct `app` package from the backend folder
repo_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_backend not in sys.path:
    sys.path.insert(0, repo_backend)

# Ensure pytest runs with project root as cwd on containerized environments
try:
    os.chdir("/app")
except Exception:
    pass

# Ensure the intended `app.models` is loaded from backend/app/models.py
try:
    import importlib.util
    import types
    app_dir = os.path.join(repo_backend, "app")
    models_file = os.path.join(app_dir, "models.py")
    if os.path.exists(models_file):
        spec = importlib.util.spec_from_file_location("app.models", models_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if "app" not in sys.modules:
            pkg = types.ModuleType("app")
            pkg.__path__ = [app_dir]
            sys.modules["app"] = pkg
        sys.modules["app.models"] = module
except Exception:
    pass

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import Item, User
from app import crud
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Item)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


# --- التعديل هنا: تغيير النطاق من module إلى function ---
@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    # Ensure the test user exists in the current DB session and has a known password
    from app.core.security import get_password_hash
    from tests.utils.utils import random_lower_string
    from app.models import UserCreate  # Import here to avoid circular imports

    password = random_lower_string()
    user = crud.get_user_by_email(session=db, email=settings.EMAIL_TEST_USER)
    
    if not user:
        # create user within the active session so test DB state is correct
        user_in = UserCreate(email=settings.EMAIL_TEST_USER, password=password)
        user = crud.create_user(session=db, user_create=user_in)
    else:
        # ensure password is updated in-place for this session
        user.hashed_password = get_password_hash(password)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Obtain token via the real login endpoint
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data={"username": settings.EMAIL_TEST_USER, "password": password})
    tokens = r.json()
    a_token = tokens.get("access_token")
    return {"Authorization": f"Bearer {a_token}"}