class AppError(Exception):
    """Base application exception"""


class QuietError(AppError):
    """Exception that should not be traced"""


class LoudError(AppError):
    """Exception that should be traced"""


class ExternalValueError(QuietError):
    """Value error that should not be traced"""
