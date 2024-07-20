from pydantic import BaseModel, AnyUrl
from typing import Optional
from datetime import datetime


class Document(BaseModel):
	title: Optional[str]
	pages: Optional[int]
	is_active: Optional[bool]
