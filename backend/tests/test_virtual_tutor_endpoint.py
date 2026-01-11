import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.api import deps
from app.models import User, StudentProgress, StudentProgressCreate

def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine

def test_virtual_tutor_endpoint():
    engine = setup_in_memory_db()
    
    # 1. Create Data
    with Session(engine) as session:
        user = User(email="client@example.com", hashed_password="x")
        session.add(user)
        session.commit()
        session.refresh(user)
        
        sp = StudentProgress.model_validate(
            StudentProgressCreate(module_name="Module A", progress=40, struggling=False), 
            update={"user_id": user.id}
        )
        session.add(sp)
        session.commit()

    # 2. Define Overrides
    def get_db_override():
        with Session(engine) as s:
            yield s

    # Override dependencies
    app.dependency_overrides[deps.get_db] = get_db_override
    app.dependency_overrides[deps.get_current_user] = lambda: user
    # Handle optional user dep if it exists
    try:
        app.dependency_overrides[deps.get_current_user_optional] = lambda: user
    except AttributeError:
        pass

    # 3. Run Test
    client = TestClient(app)
    # The fix: sending module_name as a query param
    resp = client.get("/api/v1/virtual-tutor/recommendations", params={"module_name": "Module A"})
    
    # Cleanup
    app.dependency_overrides.clear()
    
    # Assert
    assert resp.status_code == 200, f"Error: {resp.text}"
