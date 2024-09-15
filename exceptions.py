from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)



class UserNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class NotAccessException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Недостаточно прав"


class FileTooLargeException(BaseException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    detail = "Файл не должен привышать 200мб"