from pydantic import BaseModel, Field
from typing import Optional
import datetime

class User(BaseModel):
  email: str
  password: str

class Movie(BaseModel):
  """
    gt: greater than
    ge: greater than or equal
    lt: less than
    le: less than or equal
  """
  id: Optional[int] = None
  #Other way to do this
  #id: int | None = None
  title: str = Field(min_length=5, max_length=15)
  year: int = Field(le=datetime.date.today().year)
  rating: float | int = Field(ge=1, le=10)
  category: str

  # Crear valores por defecto.
  class Config():
    schema_extra = {
      "example": {
        "id": 12,
        "title": "The Godfather",
        "year": 1972,
        "rating": 8.5,
        "category": "Action"
      }
    }
