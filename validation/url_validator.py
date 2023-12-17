from models.url import Url
from typing import Type
import re
from sqlalchemy.orm import Session
from datetime import datetime
from exceptions.exceptions import UrlExpiredError, UrlInActiveError

class UrlValidator():
    def __init__(self, url: Url, db: Session):
        self.url = url
        self.db = db

    def check_status(self):
        if not self.url.is_active:
            raise UrlInActiveError('Url is inactive')

        if self.url.expire_time < datetime.now():
            raise UrlExpiredError('Url is expired')
        
        # if not self.valid_long_url(self.url.long_url):
        #     raise InvalidOriginalUrlError('Invalid original URL')
        
    # TODO: Long URL validation
    @staticmethod
    def valid_long_url(url: str):
        return True
        # url = url or 'invalid'
        # regex = re.compile(
        #     r'^(?:http|ftp)s?://'  # http:// or https://
        #     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        #     r'localhost|'  # localhost...
        #     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        #     r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        #     r'(?::\d+)?'  # optional port
        #     r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        # is_valid = regex.match(url) is not None
        # if is_valid:
        #     url = urlparse(url)
        #     allowed_path = ['contact', 'about', 'shorten', 'dashboard']
        #     if url.netloc == 'pygy.co' and url.path.strip('/') in allowed_path:
        #         return is_valid
        #     elif url.netloc in filtered_urls and url.path.strip('/') not in allowed_path:
        #         raise ValidationError('Already shortened links are not supported')
        #     else:
        #         return is_valid
