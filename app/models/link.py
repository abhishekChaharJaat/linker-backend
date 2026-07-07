from pydantic import BaseModel
from typing import Optional


class AddLinkRequest(BaseModel):
    title: str
    url: str
    category: str
    project: str
    description: Optional[str] = None
