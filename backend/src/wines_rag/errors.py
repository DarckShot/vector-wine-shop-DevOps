from fastapi import HTTPException, status


class WineNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "errorCode": "NOT_FOUND",
                "userMessage": f"Such wine doesn't exist",
            },
        )


class WineServiceError(HTTPException):
    def __init__(self, error_code: str, message: str, status_code: int = 500):
        super().__init__(
            status_code=status_code,
            detail={"errorCode": error_code, "userMessage": message},
        )
