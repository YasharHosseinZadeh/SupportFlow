from pydantic import  BaseModel,ConfigDict




class UpdateUser(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )
    id :int
    name : str
    email : str


class UserLogin(BaseModel):
    email: str
    password: str

class RoleUpdate(BaseModel):
    role: str