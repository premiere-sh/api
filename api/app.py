from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from api.database import engine
from api.models import Base
from api.endpoints import auth, users, tournaments, friends, warzone

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tournaments.router)
app.include_router(friends.router)
app.include_router(warzone.router)


@app.get('/')
def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/users/{user_id}/stats")
def stats(user_id: int):
    return {"user_id": user_id, "rank": 10, "weekly_wins": 5}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT', 'DELETE'],
    allow_headers=['*'],
)

Base.metadata.create_all(bind=engine)
