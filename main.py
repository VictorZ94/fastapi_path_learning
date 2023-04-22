from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from model import Movie, User
from typing import List
from data import movies
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "My first api with FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    data = validate_token(auth.credentials)
    if data['email'] != "admin":
      raise HTTPException(status_code=403, detail="Forbidden")


@app.get('/', tags=["Home"])
def message():
  return HTMLResponse('<h1>Hello World! changed</h1>')

@app.post("/login", tags=["Auth"])
def login(user: User):
  if user.email == "admin" and user.password == "admin":
    token: str = create_token(user.dict())
    return JSONResponse(content=token)
  return JSONResponse({"message": "Invalid user or no authenticated"})

@app.get('/movies', tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=["movies"], response_model=Movie, status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies(id: int = Path(ge=1, le=2000)) -> Movie:
  for item in movies:
    if item["id"] == id:
      return JSONResponse(status_code=200, content=item)
  return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]: #Usando parametros query
  data = [ movie for movie in movies if movie['category'].lower() == category.lower() ]
  return JSONResponse(content=data)
  #Another solution is:
  #return list(filter(lambda item: item['category'] == category , movies))

@app.post('/movies', tags=["Create new movies"], response_model=dict, status_code=201)
def create_movies(movie: Movie) -> dict:
  movies.append(movie.dict())
  return JSONResponse(status_code=201, content={"message": "Movie created successfully"})

@app.put('/movies', tags=["Update a movie"], response_model=dict, status_code=200)
def update_movies(id: int, movie: Movie) -> dict:
  for mov in movies:
    if mov["id"] == id:
      mov.update(movie)
      return JSONResponse(status_code=200, content={"message": "Movie modified successfully"})
  return "There's no movie to update"

@app.delete('/movies', tags=["Delete a movie"], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
  for item in movies:
    if item["id"] == id:
      movies.remove(item)
      return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})
  return "There's no item to delete"