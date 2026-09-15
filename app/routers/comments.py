from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.comment import CommentUpdate, CommentResponse, CommentCreate
from typing import List
from app.services.comment_service import (
    get_all_comments,
    get_comment_by_id,
    delete_comment as delete_comment_service,
    create_comment as create_comment_service,
    update_comment as update_comment_service
    )




router = APIRouter()

# creat a comment
@router.post("/tickets/{ticket_id}/comments",response_model=CommentResponse)
async def create_comment(ticket_id : int,comment_info : CommentCreate , db : AsyncSession = Depends(get_db)):

    result = await create_comment_service(db, ticket_id,comment_info)

    if result is None:
        raise HTTPException(status_code=404, detail="User or Ticket not found")


    return result



@router.get("/tickets/{ticket_id}/comments",response_model=List[CommentResponse])
async def get_comments(ticket_id : int, db : AsyncSession = Depends(get_db)
    ):
    comments = await get_all_comments(db, ticket_id)
    if comments is None:
        raise HTTPException(status_code=404, detail="User or Ticket not found")

    return comments



# get one comment
@router.get("/comments/{comment_id}",response_model=CommentResponse)
async def get_comment(comment_id : int, db : AsyncSession = Depends(get_db)):
    comment = await get_comment_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment




# update comment
@router.patch("/comments/{comment_id}",response_model=CommentResponse)
async def update_comment(comment_id : int,comment_info : CommentUpdate,db : AsyncSession = Depends(get_db)):

    comment = await update_comment_service(db, comment_id, comment_info)

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")


    return comment




# delete comment
@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id : int, db : AsyncSession = Depends(get_db)):
    comment = await delete_comment_service(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Comment deleted"}