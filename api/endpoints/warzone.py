from time import time
from typing import List
from api import models, schemas
from api.database import get_db
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from requests import get



def get_wzstatsgg_stats(warzone_user: schemas.WarzoneUser):
    #uses 3'rd party wzstats api
    #call returns 1.8mib of data per player!
    base_url = 'https://app.wzstats.gg/v2/player'
    parameters = {'username':warzone_user.username,'platform':warzone_user.platform}
    if warzone_user.platform not in ['psn','steam','xbl','battle','uno','acti']:
        raise HTTPException(status_code=422,detail='Unknown platform')
        
    response = get(base_url,params=parameters)
    if response.status_code != 200:
        raise HTTPException(status_code=404,detail='Player not found')
    
    r = response.json()
    if not (weekly_stats:=r['data']['weekly']['all']['properties']):
        #user has not played this week
        return models.WarzoneStats(
            username=warzone_user.username,
            fetched_timestamp=int(time()),
            kdRatio=0,
            kills=0,
            deaths=0,
            killsPerGame=0
        )
    return models.WarzoneStats(
            username=warzone_user.username,
            fetched_timestamp=int(time()),
            kdRatio=weekly_stats['kdRatio'],
            kills=weekly_stats['kills'],
            deaths=weekly_stats['deaths'],
            killsPerGame=weekly_stats['killsPerGame']
        )

router = APIRouter(tags=['warzone'])
@router.post('/warzone-stats/', response_model=schemas.WarzoneStats)
def get_user_stats(warzone_user: schemas.WarzoneUser,db: Session = Depends(get_db)):
    cached_stats = (
        db.query(models.WarzoneStats)
            .filter(models.WarzoneStats.username == warzone_user.username)
            .first()
    )

    if cached_stats and cached_stats['fetched_timestamp']+7200>time():
        #maximum one request every 2 hours
        return cached_stats

    new_stats = get_wzstatsgg_stats(warzone_user)

    if (db.query(models.WarzoneStats)
        .filter(models.WarzoneStats.username == warzone_user.username)
        .first()):
        (db.query(models.WarzoneStats)
            .filter(models.WarzoneStats.username == warzone_user.username)
            .update(new_stats)
        )
    else:
        db.add(new_stats)
    return new_stats
