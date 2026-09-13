from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.user import  User
from app.models.comment import Comment
from app.models.ticket import Ticket
from sqlalchemy import select
from app.schemas.comment import CommentUpdate, CommentResponse, CommentCreate
from typing import List


router = APIRouter()

# creat a comment
@router.post("/tickets/{ticket_id}/comments",response_model=CommentResponse)
async def create_comment(ticket_id : int,comment_info : CommentCreate , db : AsyncSession = Depends(get_db)):
    ticket = await db.get(Ticket, ticket_id)
    user = await db.get(User,comment_info.author_id)
    if ticket  is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    comment = Comment(
        ticket_id=ticket_id,
        content=comment_info.content,
        author_id=comment_info.author_id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return comment



@router.get("/tickets/{ticket_id}/comments",response_model=List[CommentResponse])
async def get_comments(ticket_id : int, db : AsyncSession = Depends(get_db)
    ):
    ticket = await db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    comments = await db.execute(
        select(Comment)
        .where(Comment.ticket_id == ticket_id)
    )
    result = comments.scalars().all()

    return result



# get one comment
@router.get("/comments/{comment_id}",response_model=CommentResponse)
async def get_comment(comment_id : int, db : AsyncSession = Depends(get_db)):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment




# update comment
@router.patch("/comments/{comment_id}",response_model=CommentResponse)
async def update_comment(comment_id : int,comment_info : CommentUpdate,db : AsyncSession = Depends(get_db)):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.content = comment_info.content

    await db.commit()

    await db.refresh(comment)

    return comment




# delete comment
@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id : int, db : AsyncSession = Depends(get_db)):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    await db.delete(comment)
    await db.commit()
    return {"message": "Comment deleted"}