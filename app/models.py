from datetime import datetime
from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field


class ArgDef(BaseModel):
    name: str
    type: str
    description: str


class Arg(BaseModel):
    name: str
    value: Any


class FunctionDef(BaseModel):
    name: str
    code: str
    description: str
    pkg_dependencies: List[str]
    fn_dependencies: List[str]
    args: List[ArgDef] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FunctionSummary(BaseModel):
    name: str
    description: str


class Query(BaseModel):
    query: str
    n_results: Optional[int] = 10
