from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

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

@app.get('/movies', tags=["movies"])
def get_movies():
  return movies

@app.get('/movies/{id}', tags=["movies"])
def get_movies(id: int):
  for item in movies:
    if item["id"] == id:
      return item
  return "There's no items to show"

@app.get('/movies/', tags=["movies"])
def get_movies_by_category(category: str, year: int): #Usando parametros query
  return [movie for movie in movies if movie['category'].lower() == category.lower()]
  #Another solution is:
  #return list(filter(lambda item: item['category'] == category , movies))
