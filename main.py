from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from model import Movie
from typing import List

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

@app.get('/', tags=["Home"])
def message():
  return HTMLResponse('<h1>Hello World! changed</h1>')

@app.get('/movies', tags=["movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
  return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=["movies"], response_model=Movie)
def get_movies(id: int = Path(ge=1, le=2000)) -> Movie:
  for item in movies:
    if item["id"] == id:
      return JSONResponse(content=item)
  return JSONResponse(content=[])

@app.get('/movies/', tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]: #Usando parametros query
  data = [ movie for movie in movies if movie['category'].lower() == category.lower() ]
  return JSONResponse(content=data)
  #Another solution is:
  #return list(filter(lambda item: item['category'] == category , movies))

@app.post('/movies', tags=["Create new movies"], response_model=dict)
def create_movies(movie: Movie) -> dict:
  movies.append(movie.dict())
  return JSONResponse(content={"message": "Movie created successfully"})

@app.put('/movies', tags=["Update a movie"], response_model=dict)
def update_movies(id: int, movie: Movie) -> dict:
  for mov in movies:
    if mov["id"] == id:
      mov.update(movie)
      return JSONResponse(content={"message": "Movie modified successfully"})
  return "There's no movie to update"

@app.delete('/movies', tags=["Delete a movie"], response_model=dict)
def delete_movies(id: int) -> dict:
  for item in movies:
    if item["id"] == id:
      movies.remove(item)
      return JSONResponse(content={"message": "Movie deleted successfully"})
  return "There's no item to delete"