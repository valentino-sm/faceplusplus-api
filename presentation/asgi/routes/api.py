from typing import Annotated

from fastapi import APIRouter, File
from starlette.responses import Response

from core.services.main import MainService
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from presentation.asgi.requests.api import GetCompareRequest, GetImageRequest
from presentation.asgi.responses.api import DetectResponse
from utils.logging import Logging


class APIRouterBuilder(ABCRouterBuilder):
    def __init__(
        self,
        logging: Logging,
        main_service: MainService,
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._main_service = main_service

    def create_router(self) -> APIRouter:
        router = APIRouter(prefix="/api/v1", tags=["API v1"])

        @router.post("/detect", response_model=DetectResponse)
        async def _(file: Annotated[bytes, File()]):
            """
            Detect and analyze human faces within the image that you provided.
            """
            image = await self._main_service.detect(file)
            return DetectResponse(
                id=image.id,
                face_tokens=[face.id for face in image.faces],
            )

        @router.post("/image/{id}")
        async def _(id: str, req: GetImageRequest):
            """
            Getting an image by id

            color: color of recognized faces

            faces_tokens: list of face tokens needed to be colored (default: all faces)
            """
            result = await self._main_service.build_image_by_id(
                id, req.color, req.face_tokens
            )
            return Response(content=result, media_type="image/jpeg")

        @router.post("/compare", response_model=float)
        async def _(req: GetCompareRequest):
            """
            Compare two images and return the similarity score
            """
            return await self._main_service.compare(req.face_token_1, req.face_token_2)

        @router.delete("/image/{id}", status_code=204)
        async def _(id: str):
            """
            Delete an image by id
            """
            self._logger.debug(f"Delete image by id: {id}")
            await self._main_service.delete_image_by_id(id)

        return router
