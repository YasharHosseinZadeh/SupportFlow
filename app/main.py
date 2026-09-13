from fastapi import FastAPI
from app.database import Base
from app.database import engine
from contextlib import asynccontextmanager
from app.routers.users import router as users_router
from app.routers.tickets import router as tickets_router
from app.routers.comments import router as comments_router
from app.models.user import User
from app.models.ticket import Ticket
from app.models.comment import Comment


# create async database
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



@asynccontextmanager
async def database(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="SupportFlow API",
    lifespan = database
)

app.include_router(users_router)
app.include_router(tickets_router)
app.include_router(comments_router)



# welcome
@app.get("/Welcome")
def root():
    return{"message" : "Welcome to SupportFlow API"}























