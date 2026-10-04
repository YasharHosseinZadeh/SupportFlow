from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db,require_role
from schemas.ticket import TicketResponse, TicketCreate, TicketUpdate, TicketStatusUpdate
from typing import List
from services.ticket_service import (
    get_all_tickets,
    get_ticket_by_id,
    create_ticket as create_ticket_service,
    delete_ticket as delete_ticket_service,
    update_ticket as update_ticket_service,
    get_tickets_counts_by_customer,
    update_status_ticket as update_status_ticket_service,
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
async def get_tickets(
        db: AsyncSession = Depends(get_db),
        customer_id : int | None = None,
        page : int = Query(1, ge=1),
        limit : int  = Query(10, ge=1),
):
    tickets = await get_all_tickets(db,customer_id,page,limit)
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



# Update status ticket
@router.patch("/tickets/{ticket_id}/status",response_model=TicketResponse)
async def update_ticket_status(
        ticket_id : int ,
        status : TicketStatusUpdate,
        db : AsyncSession = Depends(get_db),
        role_author = Depends(require_role("manager","agent"))
):
    ticket = await update_status_ticket_service(db, ticket_id, status)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket



# delete a ticket by id
@router.delete("/tickets/{ticket_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
        ticket_id : int,
        db: AsyncSession = Depends(get_db)
):
    ticket = await delete_ticket_service(db, ticket_id)
    if ticket is None :
        raise HTTPException(status_code=404, detail="Ticket not found")

    return