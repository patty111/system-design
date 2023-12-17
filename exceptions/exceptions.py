class UrlResourceNotFoundError(Exception):
    pass

class UrlInActiveError(Exception):
    pass

class UrlExpiredError(Exception):
    pass

class InvalidOriginalUrlError(Exception):
    pass

class UserNotExistError(Exception):
    pass