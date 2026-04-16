from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

class CleanBaseModel(BaseModel):
    def model_dump(self, *args, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
    
T = TypeVar("T")
K = TypeVar("K")

class BaseApiResponse(CleanBaseModel, Generic[T, K]):
    success: bool
    message: Optional[str] = None
    token: Optional[K] = None
    data: Optional[T] = None

