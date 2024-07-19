from uuid import UUID

from fastapi import HTTPException, status


class DBAPICallError(HTTPException):
    def __init__(self, msg: str = "..."):
        super().__init__(
            detail=f"DB api call failed: {msg}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class AppError(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )


class AppNotFoundError(AppError):
    def __init__(self, kind: str, app_id: UUID):
        super().__init__(
            detail=f"App with kind={kind} and app_id={app_id} was not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
