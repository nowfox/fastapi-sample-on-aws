import traceback
from fastapi.responses import JSONResponse
from fastapi import status, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from .enum import ErrorEnum
from . import constant
from .schemas import Error
from .logger_utils import get_logger

logger = get_logger(constant.LOGGER_API)


def response_error(code: int, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    content = Error(code=code, message=message)
    return JSONResponse(
        content=content.__dict__,
        headers=constant.HEADERS_ALLOW_ALL,
        status_code=status_code,
    )


def biz_exception(app: FastAPI):
    # customize request validation error
    @app.exception_handler(RequestValidationError)
    async def val_exception_handler(
        req: Request,
        rve: RequestValidationError,
        code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        return response_error(code, str(rve))

    # customize business error
    @app.exception_handler(BizException)
    async def biz_exception_handler(req: Request, exc: BizException):
        return response_error(exc.code, exc.message)

    # system error
    @app.exception_handler(Exception)
    async def exception_handler(req: Request, exc: Exception):
        if isinstance(exc, BizException):
            return
        error_msg = traceback.format_exc()
        logger.error(error_msg)
        return response_error(ErrorEnum.UNKNOWN_ERROR.get_code(), error_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BizException(Exception):
    def __init__(self, error: ErrorEnum, message: str = None):
        self.code = error.get_code()
        self.message = message if message is not None else error.get_message()

    def __msg__(self):
        return self.message
