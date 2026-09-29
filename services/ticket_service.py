from models.ticket import Ticket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload
from models.user import User
from schemas.ticket import TicketCreate, TicketUpdate


async def get_all_tickets(
        db: AsyncSession,
        customer_id : int | None = None,
        page : int = 1,
        limit : int = 10
):

    query = select(Ticket).options(
        selectinload(Ticket.customer)
    )

    if customer_id is not None:
        query = query.where(Ticket.customer_id == customer_id)

    query = query.offset((page - 1) * limit).limit(limit)

    tickets = await db.execute(query)
    return tickets.scalars().all()



async def get_ticket_by_id(db: AsyncSession, ticket_id: int):
    ticket = await db.execute(
        select(Ticket)
        .where(Ticket.id == ticket_id)
        .options(selectinload(Ticket.customer))
    )
    return ticket.scalar_one_or_none()


async def get_tickets_counts_by_customer(db: AsyncSession):
    tickets = select(Ticket.customer_id,func.count(Ticket.id).label("ticket_count")).group_by(Ticket.customer_id)

    result = await db.execute(tickets)

# because the result have 2 number in a row
    return [dict(row._mapping) for row in result.all()]


async def get_total_ticket_count(db: AsyncSession):
    tickets = select(func.count(Ticket.id).label("ticket_count"))
    result = await db.execute(tickets)
    return result.scalar()






async def create_ticket(db: AsyncSession, ticket_data: TicketCreate):
    customer = await db.get(User,ticket_data.customer_id)

    if customer is None:
        return None

    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        customer_id=customer.id
    )


    db.add(ticket)
    await db.commit()
    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.customer))
        .where(Ticket.id == ticket.id)
    )

    ticket = result.scalar_one()

    return ticket


async def delete_ticket(db: AsyncSession, ticket_id: int):
    ticket = await db.get(Ticket,ticket_id)

    if ticket is None:
        return None

    await db.delete(ticket)
    await db.commit()

    return ticket


async def update_ticket(db: AsyncSession, ticket_id: int, new_information: TicketUpdate):
    ticket = await db.get(Ticket,ticket_id)
    if ticket is None:
        return None
    ticket.title = new_information.title

    ticket.description = new_information.description

    await db.commit()

    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id).options(selectinload(Ticket.customer)))

    ticket = result.scalar_one()
    return ticket

