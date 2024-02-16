from app.api.core.exceptions import ApplicationException


class PaverCommandException(ApplicationException):
    """Exception class for Paver errors """

    def __init__(self, message) -> None:
        super().__init__(message)


class ExtractionErrorException(ApplicationException):
    """Exception class for errors during data extraction"""

    def __init__(self, message: str = 'Error during data extraction') -> None:
        super().__init__(message)


class TransformationErrorException(ApplicationException):
    """Exception class for errors during data transformation"""

    def __init__(self, message: str = 'Error during data transformation') -> None:
        super().__init__(message)


class LoadErrorException(ApplicationException):
    """Exception class for errors during data loading"""

    def __init__(self, message: str = 'Error during data loading') -> None:
        super().__init__(message)
