import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings


def test_create_and_list_assignments(client: TestClient, superuser_token_headers: dict[str, str]):
    # Create two assignments
    data1 = {"title": "Assignment 1", "description": "Desc 1", "module_name": "Unit 1"}
    r1 = client.post(f"{settings.API_V1_STR}/assignments/", headers=superuser_token_headers, json=data1)
    assert r1.status_code == 200
    a1 = r1.json()
    assert a1["title"] == data1["title"] or a1.get("title") == data1["title"]

    data2 = {"title": "Assignment 2", "description": "Desc 2", "module_name": "Unit 2"}
    r2 = client.post(f"{settings.API_V1_STR}/assignments/", headers=superuser_token_headers, json=data2)
    assert r2.status_code == 200

    # List assignments
    r = client.get(f"{settings.API_V1_STR}/assignments/", headers=superuser_token_headers)
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    assert len(items) >= 2


def test_submit_and_grade_flow(client: TestClient, normal_user_token_headers: dict[str, str], superuser_token_headers: dict[str, str]):
    # Create assignment as teacher/superuser
    data = {"title": "To Be Submitted", "description": "Do this", "module_name": "Unit X"}
    r = client.post(f"{settings.API_V1_STR}/assignments/", headers=superuser_token_headers, json=data)
    assert r.status_code == 200
    assignment = r.json()
    assignment_id = assignment.get("id")
    assert assignment_id is not None

    # Student submits
    submit_payload = {"content_text": "Here is my submission."}
    r_sub = client.post(f"{settings.API_V1_STR}/assignments/{assignment_id}/submit", headers=normal_user_token_headers, json=submit_payload)
    assert r_sub.status_code == 200
    sub = r_sub.json()
    assert "id" in sub
    submission_id = sub["id"]

    # Teacher grades
    grade_payload = {"id": submission_id, "grade": 85, "feedback": "Good work"}
    r_grade = client.post(f"{settings.API_V1_STR}/assignments/{assignment_id}/grade", headers=superuser_token_headers, json=grade_payload)
    assert r_grade.status_code == 200
    graded = r_grade.json()
    assert graded.get("grade") == 85
    assert graded.get("feedback") == "Good work"
