from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    external_id: str
    provider: str

    class Config:
        from_attributes = True


class TodoBase(BaseModel):
    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

