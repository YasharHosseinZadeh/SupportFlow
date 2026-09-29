from pydantic import BaseModel,ConfigDict


class CommentCreate(BaseModel):
    content: str
    author_id: int


class CommentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    content: str
    ticket_id: int
    author_id: int


class CommentUpdate(BaseModel):
    content: str