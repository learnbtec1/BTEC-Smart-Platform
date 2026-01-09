from sqlmodel import select
from app.schemas import Assessment


def test_assessment_persistence(client, db):
    payload = {
        "question": "Explain how supply and demand affect price.",
        "level": "L2",
        "major": "Business",
    }

    r = client.post("/api/v1/assessments/", json=payload)
    assert r.status_code == 200
    data = r.json()

    # Confirm record in DB
    statement = select(Assessment).where(Assessment.question == payload["question"])
    res = db.exec(statement).first()
    assert res is not None
    assert res.question == payload["question"]
    assert res.level == payload["level"]
    assert res.major == payload["major"]
