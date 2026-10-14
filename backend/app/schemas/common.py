from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

T = TypeVar("T")


class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
