from fastapi import APIRouter, Request, status, Depends, Path, HTTPException, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import update
from datetime import datetime, timedelta
from validation.url_validator import UrlValidator
from exceptions.url_exceptions import UrlExpiredError, UrlInActiveError, UrlResourceNotFoundError, InvalidOriginalUrlError
from typing import Annotated
from models.url import Url
from dbHelper import get_db
from config import config
import random

router = APIRouter(tags=["url"])

@router.get("/{short_url}",
            status_code=status.HTTP_302_FOUND,
            summary="Redirect to long URL",
            description="Redirect to long URL",
            responses={
                status.HTTP_302_FOUND: {"description": "redirect to long URL"},
                status.HTTP_404_NOT_FOUND: {"description": "link not found"},
                status.HTTP_410_GONE: {"description": "link is no longer active or expires"}
            })
async def get_url(request: Request, short_url: str, db: Session = Depends(get_db)):
    item = Url.get(db, Url.short_url == short_url)

    try:
        validaor = UrlValidator(item, db)
        validaor.field_check()
        validaor.check_status()
    except UrlResourceNotFoundError:
        raise HTTPException(status_code=404, detail="link not found")
    except (UrlInActiveError, UrlExpiredError):
        Url.update(db, Url.short_url == short_url, is_active=False)
        raise HTTPException(status_code=410, detail="link no longer active")    
    
    item.redirects += 1
    Url.update(db, item)
    
    return RedirectResponse(url=item.long_url, status_code=status.HTTP_302_FOUND)


@router.post("/shorten",
            status_code=status.HTTP_201_CREATED,
            summary="Shorten a long URL",
            description="Shorten a long URL",
            responses={
                status.HTTP_201_CREATED: {"description": "short URL created"},
                status.HTTP_400_BAD_REQUEST: {"description": "invalid long URL"}
            })
async def shorten_url(request: Request, long_url: dict = Body(...), db: Session = Depends(get_db)):

    item = Url(
        short_url = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=int(config.short_url_len))),
        long_url = long_url.get('long_url'),
        redirects = 0,
        create_time = datetime.now(),
        # expire_time = datetime.now() + timedelta(days=30),
        expire_time = 1111110,
        created_by = "123",
        is_active = True
    )


    try:
        validaor = UrlValidator(item, db)
        validaor.field_check()
        validaor.valid_long_url(item.long_url)
        Url.add(db, item)
        validaor.check_status()
    except InvalidOriginalUrlError:
        raise HTTPException(status_code=400, detail="invalid long URL, the url should not be shortened beforehand")
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail=e)

    raise HTTPException(status_code=201, detail=f"{config.base_url}/{item.short_url} is created")

@router.delete("/{short_url}", 
                status_code=status.HTTP_204_NO_CONTENT,
                summary="set a short URL to inactive",
                description="set a short URL to inactive",
                responses={
                    status.HTTP_204_NO_CONTENT: {"description": "link set to inactive"},
                    status.HTTP_404_NOT_FOUND: {"description": "link not found"}
                })
async def inactive_shorturl(request: Request, short_url: str, db: Session = Depends(get_db)):
    item = Url.get(db, Url.short_url == short_url)
    
    try:
        validaor = UrlValidator(item, db)
        validaor.field_check()
        validaor.check_status()
    except UrlResourceNotFoundError:
        raise HTTPException(status_code=404, detail="link not found")
    except:
        pass

    Url.update(db, Url.short_url == short_url, is_active=False)    
    raise HTTPException(status_code=204)    # dont include detail in response body for 204