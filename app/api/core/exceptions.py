

class ApplicationException(Exception):
    """Base Exception class to manage custom exceptions"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotFoundException(ApplicationException):
    """Exception class used for nonexistent records"""

    def __init__(self, message: str = 'Record not found') -> None:
        super().__init__(message)


class DatabaseErrorException(ApplicationException):
    """Exception class used for database errors"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoConnectionDatabaseException(ApplicationException):
    """Exception class used for No connection to database"""

    def __init__(self, message: str = "Connection is not established.") -> None:
        super().__init__(message)
