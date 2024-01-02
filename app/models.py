from pydantic import BaseModel


class FunctionBase(BaseModel):
    name: str
    code: str
    description: str
    dependencies: list[str]
