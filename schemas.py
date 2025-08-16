from pydantic import BaseModel, EmailStr

class Response(BaseModel):
    id: int
    username: str