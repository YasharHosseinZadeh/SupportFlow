from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.comment import CommentCreate, CommentUpdate


async def get_all_comments(db: AsyncSession, ticket_id: int):
    ticket = await db.get(Ticket, ticket_id)
    if ticket is None:
        return None

    comments = await db.execute(
        select(Comment)
        .where(Comment.ticket_id == ticket.id)
    )
    result = comments.scalars().all()
    return result



async def get_comment_by_id(db: AsyncSession, comment_id: int):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        return None

    return comment



async def create_comment(db: AsyncSession, ticket_id: int, comment_info: CommentCreate):
    ticket = await db.get(Ticket, ticket_id)

    user = await db.get(User,comment_info.author_id)

    if user is None:
        return None

    if ticket is None:
        return None

    comment = Comment(
        ticket_id = ticket_id,
        content = comment_info.content,
        author_id = comment_info.author_id
    )

    db.add(comment)

    await db.commit()
    await db.refresh(comment)

    return comment


async def delete_comment(db: AsyncSession, comment_id: int):
    comment = await db.get(Comment, comment_id)

    if comment is None:
        return None

    await db.delete(comment)
    await db.commit()

    return comment


async def update_comment(db: AsyncSession, comment_id: int, comment_info: CommentUpdate):
    comment = await db.get(Comment, comment_id)
    if comment is None:
        return None

    comment.content = comment_info.content

    await db.commit()
    return comment