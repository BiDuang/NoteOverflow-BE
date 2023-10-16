from sqlalchemy.orm import Session

from models.database import User, Note


# noinspection PyTypeChecker
def get_username(id: int, db: Session) -> str | None:
    if db.query(User).filter(User.id == id).first() is not None:
        return db.query(User).filter(User.id == id).first().usr
    return None


def get_note_author(id: int, db: Session) -> int | None:
    if db.query(Note).filter(Note.id == id).first() is not None:
        return db.query(Note).filter(Note.id == id).first().author_id
    return None
