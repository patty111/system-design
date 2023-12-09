from pydantic import BaseModel

class URLAddSchema(BaseModel):
    long_url: str
    short_url: str
    is_active: bool
    expire_time: datetime
    created_by: str