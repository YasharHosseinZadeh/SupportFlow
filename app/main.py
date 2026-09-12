from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import User
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.database import Base
from app.models.user import User
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine
from app.schemas.ticket import TicketCreate,TicketUpdate,TicketResponse
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.orm import selectinload


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


# welcome
@app.get("/Welcome")
def root():
    return{"message" : "Welcome to SupportFlow API"}


# create a user and save in database
@app.post("/users")
async def create_user(
    name : str,
    email : str,
    db : AsyncSession = Depends(get_db)
):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)


    return user


# read all users
@app.get("/users")
async def get_users(db: AsyncSession= Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users



@app.get("/users/{user_id}")
async def get_user(user_id : int, db: AsyncSession = Depends(get_db)):
    result = await db.get(User, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")


    return result





class UpdateUser(BaseModel):
    name: str
    email: str

# update the user's information
@app.patch("/users/{user_id}")
async def update_user(
    user_id : int,
    new_information : UpdateUser,
    db : AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = new_information.name

    user.email = new_information.email

    await db.commit()

    await db.refresh(user)

    return user


# delete a user by id
@app.delete("/users/{user_id}")
async def delete_user(
    user_id : int,
    db : AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)

    await db.commit()

    return {"message": "User deleted"}



# create a ticket
@app.post("/tickets")
async def create_ticket(
        ticket_data : TicketCreate,
        db : AsyncSession = Depends(get_db)
):
    customer = await db.get(User, ticket_data.customer_id)
    if customer is None:
        raise HTTPException(status_code=400, detail="Customer id is wrong")
    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        customer_id=ticket_data.customer_id)

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket





# read all ticket and users info
@app.get("/tickets",response_model=List[TicketResponse])
async def get_tickets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Ticket).options(selectinload(Ticket.customer))
    )
    tickets = result.scalars().all()
    return tickets



# read a specific ticket with user info  by id
@app.get("/tickets/{ticket_id}",response_model=TicketResponse)
async def get_ticket(ticket_id : int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Ticket)
        .where(Ticket.id == ticket_id)
        .options(selectinload(Ticket.customer))
    )
    ticket = result.scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket



#update the ticket's information
@app.patch("/tickets/{ticket_id}")
async def update_ticket(
    ticket_id : int,
    new_information : TicketUpdate,
    db : AsyncSession= Depends(get_db)
):
    ticket = await db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.title = new_information.title

    ticket.description = new_information.description

    await db.commit()
    await db.refresh(ticket)

    return ticket




# delete a ticket by id
@app.delete("/tickets/{ticket_id}")
async def delete_ticket(
        ticket_id : int,
        db: AsyncSession = Depends(get_db)
):
    ticket = await db.get(Ticket, ticket_id)
    if ticket is None :
        raise HTTPException(status_code=404, detail="Ticket not found")
    await db.delete(ticket)
    await db.commit()
    return {"message": "Ticket deleted"}