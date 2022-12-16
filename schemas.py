from typing import Optional
from pydantic import BaseModel, Field

class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt = 0, lt = 6, description = 'Must be between 1 and 5')
    complete: bool

class NewUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
