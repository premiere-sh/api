from typing import List
from api import models, schemas
from api.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(tags=['warzone'])


@router.post('/warzone-stats/', response_model=schemas.Stats)
def get_user_stats(warzone_user: schemas.WarzoneUser):
    stats = {}
    return stats

