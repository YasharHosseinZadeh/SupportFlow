from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.ticket import TicketResponse, TicketCreate, TicketUpdate
from typing import List
from app.services.ticket_service import (
    get_all_tickets,
    get_ticket_by_id,
    create_ticket as create_ticket_service,
    delete_ticket as delete_ticket_service,
    update_ticket as update_ticket_service
)

router = APIRouter()




# create a ticket
@router.post("/tickets",response_model=TicketResponse)
async def create_ticket(
        ticket_data : TicketCreate,
        db : AsyncSession = Depends(get_db)
):
    result = await create_ticket_service(db, ticket_data)
    if result is None:
        raise HTTPException(status_code=400, detail="Customer id is wrong")

    return result


# read all ticket and users info
@router.get("/tickets",response_model=List[TicketResponse])
async def get_tickets(db: AsyncSession = Depends(get_db)):
    tickets = await get_all_tickets(db)
    return tickets



# read a specific ticket with user info  by id
@router.get("/tickets/{ticket_id}",response_model=TicketResponse)
async def get_ticket(ticket_id : int, db: AsyncSession = Depends(get_db)):
    result = await get_ticket_by_id(db, ticket_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return result



#update the ticket's information
@router.patch("/tickets/{ticket_id}",response_model=TicketResponse)
async def update_ticket(
    ticket_id : int,
    new_information : TicketUpdate,
    db : AsyncSession= Depends(get_db)
):
    ticket = await update_ticket_service(db, ticket_id, new_information)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket




# delete a ticket by id
@router.delete("/tickets/{ticket_id}")
async def delete_ticket(
        ticket_id : int,
        db: AsyncSession = Depends(get_db)
):
    ticket = await delete_ticket_service(db, ticket_id)
    if ticket is None :
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deleted"}
