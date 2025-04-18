from __future__ import annotations

__all__ = ("InvalidTokenError", "TrelloError")


class TrelloError(Exception):
    """Base class for all Trello API related errors.

    Attributes:
        status_code: HTTP status code associated with the error.
        message: Error message describing the issue.
    """

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class InvalidTokenError(TrelloError):
    """Exception raised when an invalid token is provided."""

    def __init__(self) -> None:
        super().__init__(401)

    def __str__(self) -> str:
        return "Invalid token provided. Either the user has revoked it or it is incorrect."


def raise_for_status_code(status_code: int) -> None:
    """Raises an appropriate error based on the HTTP status code.

    Args:
        status_code: The HTTP status code to check.

    Raises:
        TrelloError: If the status code indicates an error.
    """
    match status_code:
        case 401:
            raise InvalidTokenError
        case _:
            raise TrelloError(status_code)
