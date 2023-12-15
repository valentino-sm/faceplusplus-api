from typing import Protocol

import cv2
import numpy as np
from pydantic_extra_types.color import Color

from core.models.image import Image
from utils.logging import Logging


class ABCImageService(Protocol):
    async def draw(self, image: Image, color: Color, faces: list[str] | None) -> bytes:
        raise NotImplementedError


class ImageService(ABCImageService):
    def __init__(self, logging: Logging):
        self._logger = logging.get_logger(__name__)

    async def draw(self, image: Image, color: Color, faces: list[str] | None) -> bytes:
        if not faces:
            faces = [face.id for face in image.faces]
        faces_set = set(faces)
        self._logger.debug(f"Drawing image with {len(faces_set)} faces")
        r, g, b = color.as_rgb_tuple(alpha=False)  # type: ignore

        nparr = np.frombuffer(image.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        for face in image.faces:
            if face.id not in faces_set:
                continue
            x, y, w, h = face.x, face.y, face.width, face.height
            cv2.rectangle(img, (x, y), (x + w, y + h), (b, g, r), 2)
        return cv2.imencode(".jpg", img)[1].tobytes()
