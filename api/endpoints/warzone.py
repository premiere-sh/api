from time import time
from typing import List
from api import models, schemas
from api.database import get_db
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from requests import get



router = APIRouter(tags=['warzone'])
@router.post('/warzone-stats/', response_model=schemas.WarzoneStats)
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
    
    stats={
        "username"         :warzone_user.username,
        "fetched_timestame":time(),
        "kdRatio"          :r["kdRatio"],
        "kills"            :r["kills"],
        "deaths"           :r["deaths"],
        "killsPerGame"     :r["killsPerGame"]
    }
    (db.query(models.WarzoneStats)
        .filter(models.WarzoneStats.username == warzone_user.username)
        .update(stats)
    )
    return stats


def get_stats_from_db(warzone_user: schemas.WarzoneUser,db: Session = Depends(get_db)):
    db_wzStats = (
        db.query(models.WarzoneStats)
            .filter(models.WarzoneStats.username == warzone_user.username).first()
    )
    return db_wzStats

def get_user_stats(warzone_user: schemas.WarzoneUser,db: Session = Depends(get_db)):
    stats = get_stats_from_db(warzone_user)
    if not stats or stats['fetched_timestame']+7200>time():
        stats = update_stats_wzstatsgg(warzone_user=warzone_user,db=db)
    return stats