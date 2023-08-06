from typing import List, Optional
from pydantic import BaseModel

class Token(BaseModel):
    roles: List[str]
    scopes: List[str]
    user: Optional[int]
    app: Optional[int]

