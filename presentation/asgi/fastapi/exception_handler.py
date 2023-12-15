from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from presentation.asgi.responses.base import BaseResponse
from utils.exceptions import AppError

responses = {
    400: {"model": BaseResponse},
    500: {"model": BaseResponse},
}


async def exception_handler(request: Request, exception: Exception) -> Response:
    match exception:
        case AppError():
            return JSONResponse(status_code=400, content={"message": str(exception)})
        case _:
            return JSONResponse(
                status_code=500, content={"message": "Internal server error"}
            )
