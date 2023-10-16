from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime

from database.main import get_db
from models.database import User, Note, Comment
from models.note import NoteInfo, UpdateContent, PostContent, CommentInfo
from utils.security import get_current_user
from utils.user import get_username, get_note_author

note_router = APIRouter(prefix="/note")


@note_router.get("/")
async def get_notes(db: Session = Depends(get_db)):
    return [NoteInfo(id=i.id, author=get_username(i.id, db), content=i.content, update_at=i.update_at) for i in
            db.query(Note).all()]


@note_router.post("/new")
async def create_note(body: PostContent, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.add(Note(author_id=None if body.is_anonymous else current_user.id,
                content=body.content, update_at=datetime.now()))
    db.commit()
    return Response(status_code=201)


@note_router.put("/{note_id}")
async def update_note(note_id: int, body: UpdateContent, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.author_id != current_user.id:
        return HTTPException(status_code=403, detail="You are not the author of this note")
    note.content = body.content
    note.update_at = datetime.now()
    db.commit()
    return Response(status_code=200)


@note_router.delete("/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.author_id != current_user.id:
        return HTTPException(status_code=403, detail="You are not the author of this note")
    db.delete(note)
    db.commit()
    return Response(status_code=200)


@note_router.get("/{note_id}/comments")
async def get_comments(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return [CommentInfo(id=i.id, note_id=i.note_id, author=get_username(i.author_id, db), content=i.content,
                        update_at=i.update_at) for i in db.query(Comment).filter(Comment.note_id == note_id).all()]


@note_router.post("/{note_id}/comment")
async def create_comment(note_id: int, body: PostContent, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.add(Comment(author_id=None if body.is_anonymous else current_user.id, note_id=note_id, content=body.content,
                   update_at=datetime.now()))
    db.commit()
    return Response(status_code=201)


@note_router.put("/comment/{comment_id}")
async def update_comment(comment_id: int, body: UpdateContent, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to update this comment")
    comment.content = body.content
    comment.update_at = datetime.now()
    db.commit()
    return Response(status_code=200)


@note_router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, note_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id and get_note_author(note_id, db) != current_user.id:
        raise HTTPException(status_code=403, detail="You have no permission to delete this comment")
    db.delete(comment)
    db.commit()
    return Response(status_code=200)
