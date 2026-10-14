from fastapi import HTTPException, status


class BusinessError(HTTPException):
    def __init__(self, message: str = "Business logic error", code: str = "BUSINESS_ERROR"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": message, "code": code})


class NotFoundError(HTTPException):
    def __init__(self, resource: str = "Resource", resource_id: str = ""):
        detail = f"{resource} not found"
        if resource_id:
            detail = f"{resource} '{resource_id}' not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail={"message": detail, "code": "NOT_FOUND"})


class AuthError(HTTPException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": message, "code": "AUTH_ERROR"},
            headers={"WWW-Authenticate": "Bearer"},
        )


class ValidationError(HTTPException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"message": message, "code": "VALIDATION_ERROR"})
