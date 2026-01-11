import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.api import deps
from app.models import User

def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine

def test_assistant_query():
    engine = setup_in_memory_db()
    with Session(engine) as session:
        user = User(email="assistant@example.com", hashed_password="x")
        session.add(user)
        session.commit()
        session.refresh(user)

        app.dependency_overrides[deps.get_current_user] = lambda: user
        try:
            app.dependency_overrides[deps.get_current_user_optional] = lambda: user
        except AttributeError:
            pass

        client = TestClient(app)
        res = client.post("/api/v1/assistant/query", json={"prompt": "Hello plan"})
        
        app.dependency_overrides.clear()
        assert res.status_code == 200

def test_upload_file():
    engine = setup_in_memory_db()
    with Session(engine) as session:
        user = User(email="uploader@example.com", hashed_password="x")
        session.add(user)
        session.commit()
        session.refresh(user)
    
        app.dependency_overrides[deps.get_current_user] = lambda: user
        
        client = TestClient(app)
        files = {'file': ('test.txt', b'content', 'text/plain')}
        res = client.post("/api/v1/files/upload", files=files)
        
        app.dependency_overrides.clear()
        assert res.status_code in [200, 201]
