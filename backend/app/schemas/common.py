from pydantic import BaseModel


class PageMeta(BaseModel):
    total: int
    page: int
    size: int
    pages: int


class Message(BaseModel):
    message: str
