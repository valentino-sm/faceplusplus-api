from typing import Any, Sequence, TypeVar

from pydantic import TypeAdapter

from core.models.image import Image
from infrastructure.db.abc_repository import BaseRepository
from infrastructure.db.models.models import Face as FaceModel
from infrastructure.db.models.models import Image as ImageModel
from utils.logging import Logging

T = TypeVar("T")


class ImageRepository:
    def __init__(
        self,
        logging: Logging,
        repository: BaseRepository,  # type: ignore - hack for DI
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._repository: BaseRepository[ImageModel] = repository
        self._type_adapter = TypeAdapter(Image)

    async def create_image(self, image: Image) -> ImageModel:
        image_obj = await self._repository.create_obj(
            ImageModel, **image.model_dump(exclude={"faces"})
        )
        for face in image.faces:
            await self._repository.create_obj(
                FaceModel,  # type: ignore
                image_id=image.id,
                **face.model_dump(),
            )
        return image_obj

    async def get_image_by_id(self, id_: str) -> Image:
        image_obj = await self._repository.get_by_id(ImageModel, id_)
        return self._type_adapter.validate_python(image_obj, from_attributes=True)

    async def get_all_images(self) -> Sequence[ImageModel]:
        return await self._repository.get_all(ImageModel)

    async def update_image(self, id_: str, **kwargs: Any) -> None:
        await self._repository.update_obj(ImageModel, id_, **kwargs)

    async def delete_image(self, id_: str):
        await self._repository.delete_obj(ImageModel, id_)
