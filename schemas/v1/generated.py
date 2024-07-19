from pydantic import BaseModel, EmailStr, AnyUrl
from typing import Optional
from datetime import datetime


class Person(BaseModel):
	name: str
	age: int
	email: Optional[EmailStr]
	is_active: Optional[bool]
