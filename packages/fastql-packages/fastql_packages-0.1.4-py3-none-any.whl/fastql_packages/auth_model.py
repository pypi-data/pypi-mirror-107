import pydantic
from typing import Optional, Any
class AuthorizationResult(pydantic.BaseModel):
    authenticated: bool = False
    message: Optional[str] = None
    status: int = 0
    auth: Any = None