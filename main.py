from fastapi import FastAPI
from database import Base
from database import engine
from contextlib import asynccontextmanager
from routers.users import router as users_router
from routers.tickets import router as tickets_router
from routers.comments import router as comments_router
from routers.analytics import router as analytics_router
from models.user import User
from models.ticket import Ticket
from models.comment import Comment


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
app.include_router(analytics_router)


# welcome
@app.get("/Welcome")
def root():
    return{"message" : "Welcome to SupportFlow API"}























