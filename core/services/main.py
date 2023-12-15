from pydantic_extra_types.color import Color

from core.models.image import Image
from core.services.image import ABCImageService
from infrastructure.cognitive_service import ABCCognitiveService
from infrastructure.db.exceptions import exc
from infrastructure.db.repositories.image import ImageRepository
from infrastructure.db.session_manager import ABCSessionManager
from utils.logging import Logging


class MainService:
    def __init__(
        self,
        logging: Logging,
        session_manager: ABCSessionManager,
        cognitive_service: ABCCognitiveService,
        image_repository: ImageRepository,
        image_service: ABCImageService,
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._session_manager = session_manager
        self._cognitive_service = cognitive_service
        self._image_repository = image_repository
        self._image_service = image_service

    async def detect(self, image_file: bytes) -> Image:
        image = await self._cognitive_service.detect(image_file)
        async with self._session_manager.make_session():
            try:
                await self._image_repository.create_image(image)
            except exc.IntegrityError:
                self._logger.debug("Image already exists")
        return image

    async def build_image_by_id(
        self, id_: str, color: Color | None, faces_ids: list[str] | None
    ) -> bytes:
        async with self._session_manager.make_session():
            image = await self._image_repository.get_image_by_id(id_)
        if color is None:
            return image.data
        return await self._image_service.draw(image, color, faces_ids)

    async def compare(self, face_token_1: str, face_token_2: str):
        return await self._cognitive_service.compare(face_token_1, face_token_2)

    async def delete_image_by_id(self, id_: str):
        async with self._session_manager.make_session():
            await self._image_repository.delete_image(id_)
