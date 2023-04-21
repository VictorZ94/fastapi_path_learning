from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import datetime

app = FastAPI()
app.title = "My first api with FastAPI"
app.version = "0.0.1"

movies = [
    {
      "id": 1,
      "title": "The Godfather",
      "year": 1972,
      "rating": 8.5,
      "category": "Action"
    },
    {
      "id": 2,
      "title": "The Godfather: Part II",
      "year": 1974,
      "rating": 8.5,
      "category": "Sci Fic"
    },
    {
      "id": 3,
      "title": "The Godfather: Part III",
      "year": 1975,
      "rating": 8.5,
      "category": "Thriller"
    },
    {
      "id": 4,
      "title": "The Godfather: Part IV",
      "year": 1976,
      "rating": 8.5,
      "category": "Comedy"
    },
    {
      "id": 5,
      "title": "The Godfather: Part V",
      "year": 1977,
      "rating": 9.5,
      "category": "Action"
    }
  ]

class Movie(BaseModel):
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

@app.get('/', tags=["Home"])
def message():
  return HTMLResponse('<h1>Hello World! changed</h1>')

@app.get('/movies', tags=["movies"])
def get_movies():
  return movies

@app.get('/movies/{id}', tags=["movies"])
def get_movies(id: int = Path(ge=1, le=2000)):
  for item in movies:
    if item["id"] == id:
      return item
  return "There's no items to show"

@app.get('/movies/', tags=["movies"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)): #Usando parametros query
  return [movie for movie in movies if movie['category'].lower() == category.lower()]
  #Another solution is:
  #return list(filter(lambda item: item['category'] == category , movies))

@app.post('/movies', tags=["Create new movies"])
def create_movies(movie: Movie):
  movies.append(movie.dict())
  return movie

@app.put('/movies', tags=["Update a movie"])
def update_movies(id: int, movie: Movie):
  for mov in movies:
    if mov["id"] == id:
      mov.update(movie)
      return mov
  return "There's no item to update"

@app.delete('/movies', tags=["Delete a movie"])
def delete_movies(id: int):
  for item in movies:
    if item["id"] == id:
      movies.remove(item)
      return "Item deleted"
  return "There's no item to delete"