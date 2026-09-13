from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.user import  User
from app.models.ticket import Ticket
from sqlalchemy import select
from app.schemas.ticket import TicketResponse, TicketCreate, TicketUpdate
from typing import List
from sqlalchemy.orm import selectinload

router = APIRouter()




# create a ticket
@router.post("/tickets",response_model=TicketResponse)
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
@router.get("/tickets",response_model=List[TicketResponse])
async def get_tickets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Ticket).options(selectinload(Ticket.customer))
    )
    tickets = result.scalars().all()
    return tickets



# read a specific ticket with user info  by id
@router.get("/tickets/{ticket_id}",response_model=TicketResponse)
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
@router.patch("/tickets/{ticket_id}",response_model=TicketResponse)
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
@router.delete("/tickets/{ticket_id}")
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
