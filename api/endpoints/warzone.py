from time import time
from typing import List
from wsgiref.util import request_uri
from api import models, schemas
from api.database import get_db
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from requests import get



def update_stats_wzstatsgg(warzone_user: schemas.WarzoneUser,db: Session = Depends(get_db)):
    #uses 3'rd party wzstats api
    #call returns 1.8mib of data per player!
    base_url = 'https://app.wzstats.gg/v2/player'
    parameters = {"username":warzone_user.username,"platform":warzone_user.platform}
    response = get(base_url,params=parameters)
    if response.status_code != 200:
        raise HTTPException(status_code=404,detail="Player not found")
    
    r = response.json()
    r=r["data"]["weekly"]["all"]["properties"]
    db_stats = models.WarzoneStats(
        username=warzone_user.username,
        fetched_timestamp=int(time()),
        kdRatio=r["kdRatio"],
        kills=r["kills"],
        deaths=r["deaths"],
        killsPerGame=r["killsPerGame"]
    )
    if db.query(models.WarzoneStats).filter(models.WarzoneStats.username == warzone_user.username).first():
        (db.query(models.WarzoneStats)
            .filter(models.WarzoneStats.username == warzone_user.username)
            .update(db_stats)
        )
    else:
        db.add(db_stats)

    return db_stats


router = APIRouter(tags=['warzone'])
@router.post('/warzone-stats/', response_model=schemas.WarzoneStats)
def get_user_stats(warzone_user: schemas.WarzoneUser,db: Session = Depends(get_db)):
    cached_stats = (
        db.query(models.WarzoneStats)
            .filter(models.WarzoneStats.username == warzone_user.username)
            .first()
    )
    if cached_stats:
        if cached_stats['fetched_timestamp']+7200>time():
            return cached_stats
    
    return update_stats_wzstatsgg(warzone_user,db)
