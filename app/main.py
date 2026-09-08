from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import User
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.database import Base
from app.models.user import User
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.database import engine
from app.schemas.ticket import TicketCreate,TicketUpdate,TicketResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SupportFlow API")


# welcome
@app.get("/Welcome")
def root():
    return{"message" : "Welcome to SupportFlow API"}

# create a user and save in database
@app.post("/users")
def create_user(
    name : str,
    email : str,
    db : Session = Depends(get_db)
):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)


    return user


# read all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


class UpdateUser(BaseModel):
    name: str
    email: str

# update the user's information
@app.patch("/users/{user_id}")
def update_user(
    user_id : int,
    new_information : UpdateUser,
    db : Session = Depends(get_db)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = new_information.name

    user.email = new_information.email

    db.commit()

    db.refresh(user)

    return user


# delete a user by id
@app.delete("/users/{user_id}")
def delete_user(
    user_id : int,
    db : Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}



# create a ticket
@app.post("/tickets")
def create_ticket(
        ticket_data : TicketCreate,
        db : Session = Depends(get_db)
):
    customer = db.get(User, ticket_data.customer_id)
    if customer is None:
        raise HTTPException(status_code=400, detail="Customer id is wrong")
    ticket = Ticket(title=ticket_data.title, description=ticket_data.description, customer_id=ticket_data.customer_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket



# read all tickets
@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):

    tickets = db.query(Ticket).all()

    return tickets



# read all ticket and users info
@app.get("/tickets",response_model=List[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return tickets



# read a specific ticket with user info  by id
@app.get("/tickets/{ticket_id}",response_model=TicketResponse)
def get_ticket(ticket_id : int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


#update the ticket's information
@app.patch("/tickets/{ticket_id}")
def update_ticket(
    ticket_id : int,
    new_information : TicketUpdate,
    db : Session = Depends(get_db)
):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.title = new_information.title

    ticket.description = new_information.description

    db.commit()
    db.refresh(ticket)

    return ticket




# delete a ticket by id
@app.delete("/tickets/{ticket_id}")
def delete_ticket(
        ticket_id : int,
        db: Session = Depends(get_db)
):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None :
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted"}