from typing import Any, List, Dict
from pydantic import BaseModel, Field


class FunctionSubmission(BaseModel):
    name: str
    code: str
    description: str
    dependencies: List[str]


class FunctionExecution(BaseModel):
    name: str
    args: Dict[str, Any] = Field(default_factory=list)
