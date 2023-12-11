from fastapi import APIRouter, Request, status, Depends, Path, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlmodel import select, update, insert, Session, col
from datetime import datetime, timedelta
from validation.url_validator import UrlValidator
from exceptions.url_exceptions import UrlExpiredError, UrlInActiveError, UrlResourceNotFoundError, InvalidOriginalUrlError
from typing import Annotated
from models.url import Url
from dbHelper import get_db
from config import config
import hashlib
import random

router = APIRouter(tags=["url"])
base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shortener(long_url: str) -> str:
    hash_res = hashlib.md5(long_url.encode('utf-8')).hexdigest()
    num = int(hash_res, 16)

    result_str = ""
    while num:
        result_str = f"{base62[num % 62]}{result_str}"
        num = num // 62
    return result_str[:8]


@router.get("/{short_url}",
            status_code=status.HTTP_302_FOUND,
            summary="Redirect to long URL",
            description="Redirect to long URL",
            responses={
                status.HTTP_302_FOUND: {"description": "redirect to long URL"},
                status.HTTP_404_NOT_FOUND: {"description": "link not found"},
                status.HTTP_410_GONE: {"description": "link is no longer active or expires"}
            })
async def get_url(request: Request, short_url: str, db: Session = Depends(get_db)): # One session per Request!
    stmt = select(Url).where(col(Url.short_url) == short_url)
    item = db.exec(stmt).one_or_none()

    if item is None:
        raise HTTPException(status_code=404, detail="link not found")

    try:
        validaor = UrlValidator(item, db)
        validaor.check_status()
    except (UrlInActiveError, UrlExpiredError):
        item.is_active = False
        db.add(item)
        db.commit()
        db.refresh(item)
        raise HTTPException(status_code=410, detail="link no longer active")    
    
    stmt = update(Url).where(Url.short_url == short_url).values(redirects=item.redirects+1)
    db.exec(stmt)
    db.commit()

    return RedirectResponse(url=item.long_url, status_code=status.HTTP_302_FOUND)


@router.post("/shorten",
            status_code=status.HTTP_201_CREATED,
            summary="Shorten a long URL",
            description="Shorten a long URL",
            responses={
                status.HTTP_201_CREATED: {"description": "short URL created"},
                status.HTTP_400_BAD_REQUEST: {"description": "invalid long URL"},
            })
async def shorten_url(request: Request, long_url: str = Form(...), db: Session = Depends(get_db)):

    item = Url(
        short_url = shortener(long_url),
        long_url = long_url,
        redirects = 0,
        create_time = datetime.now(),
        expire_time = datetime.now() + timedelta(days=30),
        created_by = "123",
        is_active = True
    )
    
    try:
        validaor = UrlValidator(item, db)
        validaor.valid_long_url(item.long_url)
        validaor.check_status()

    except InvalidOriginalUrlError:
        raise HTTPException(status_code=400, detail="invalid long URL, the url should not be shortened beforehand")
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400)

    db.add(item)
    db.commit()

    raise HTTPException(status_code=201, detail=f"{config.base_url}/{item.short_url}")


@router.delete("/{short_url}", 
                status_code=status.HTTP_204_NO_CONTENT,
                summary="set a short URL to inactive",
                description="set a short URL to inactive",
                responses={
                    status.HTTP_204_NO_CONTENT: {"description": "link set to inactive"},
                    status.HTTP_404_NOT_FOUND: {"description": "link not found"}
                })
async def inactive_shorturl(request: Request, short_url: str, db: Session = Depends(get_db)):
    stmt = select(Url).where(col(Url.short_url) == short_url)
    item = db.exec(stmt).one_or_none()
    
    try:
        validaor = UrlValidator(item, db)
        validaor.check_status()
    except UrlResourceNotFoundError:
        raise HTTPException(status_code=404, detail="link not found")
    except:
        pass

    item.is_active = False
    db.add(item)
    db.commit()
    db.refresh(item)
    raise HTTPException(status_code=204)