from pydantic import BaseModel, AnyUrl
from typing import Optional
from datetime import datetime


class Person(BaseModel):
	name: str
	age: int
	email: Optional[str]
	is_active: Optional[bool]
