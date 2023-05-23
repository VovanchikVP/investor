from pydantic import BaseModel


class ExampleSchema(BaseModel):
    name: str = None
    date: str
