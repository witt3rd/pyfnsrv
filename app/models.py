from datetime import datetime
from typing import Any, List, Dict
from pydantic import BaseModel, Field


class FunctionSubmission(BaseModel):
    name: str
    code: str
    description: str
    dependencies: List[str]
    args: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FunctionExecution(BaseModel):
    name: str
    args: Dict[str, Any] = Field(default_factory=list)
