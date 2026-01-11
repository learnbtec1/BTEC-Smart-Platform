from typing import Any, Dict, List

from sqlmodel import Session, select

from app import crud
from app.models import Item, ItemCreate


def get_examples_for_user(session: Session, user_id: str) -> List[Dict[str, Any]]:
    """Return items owned by the user (small projection)."""
    stmt = select(Item).where(Item.owner_id == user_id)
    rows = session.exec(stmt).all()
    return [ {"id": str(r.id), "title": r.title, "description": r.description} for r in rows]


def create_example_item(session: Session, owner_id: str, item_in: ItemCreate) -> Dict[str, Any]:
    """Create an `Item` using existing CRUD helper and return a serializable dict."""
    db_item = crud.create_item(session=session, item_in=item_in, owner_id=owner_id)
    return {"id": str(db_item.id), "title": db_item.title, "description": db_item.description}
