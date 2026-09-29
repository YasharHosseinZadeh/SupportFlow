from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from services.ticket_service import (
    get_tickets_counts_by_customer,
    get_total_ticket_count as get_total_ticket_count_service)

router = APIRouter()

# Get how many tickets each customer has
@router.get("/analytics/tickets")
async def get_customer_tickets(db: AsyncSession = Depends(get_db)):
    tickets = await get_tickets_counts_by_customer(db)
    return tickets


# Get the total of tickets
@router.get("/analytics/tickets/total")
async def get_total_ticket_count(db: AsyncSession = Depends(get_db)):
    ticket_count = await get_total_ticket_count_service(db)
    return ticket_count