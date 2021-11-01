from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from api.database import engine
from api.models import Base
from api.routers import auth, users, tournaments, friends

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tournaments.router)
# app.include_router(friends.router)

Base.metadata.create_all(bind=engine) 


@app.get('/')
def docs_redirect():
    return RedirectResponse(url='/docs')

