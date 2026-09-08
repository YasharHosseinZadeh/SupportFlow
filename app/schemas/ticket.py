from pydantic import BaseModel,ConfigDict


class TicketCreate(BaseModel):
    title: str
    description: str
    customer_id: int



class TicketUpdate(BaseModel):
    title: str
    description: str



class CustomerResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes= True
    )
    id: int
    name: str
    email: str



class TicketResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes= True
    )
    id: int
    title: str
    description: str
    customer_id: int

    # customer must be same name as customer in Ticket table and in User table (back_populates = "customer")
    customer : CustomerResponse