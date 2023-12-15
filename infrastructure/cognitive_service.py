from typing import Protocol

from core.models.image import Face, Image
from infrastructure.http import ABCHTTPClient
from utils.exceptions import ExternalValueError
from utils.logging import Logging


class ABCCognitiveService(Protocol):
    async def detect(self, image: bytes) -> Image:
        raise NotImplementedError

    async def compare(self, face_token_1: str, face_token_2: str) -> float:
        raise NotImplementedError


class FacePlusPlusCognitiveService(ABCCognitiveService):
    def __init__(
        self,
        logging: Logging,
        http_client: ABCHTTPClient,
        api_key: str,
        api_secret: str,
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._http_client = http_client

        self._api_url = "https://api-us.faceplusplus.com/facepp/v3"
        self._api_params = {"api_key": api_key, "api_secret": api_secret}

    async def detect(self, image: bytes) -> Image:
        result = await self._http_client.post(
            url=f"{self._api_url}/detect",
            params=self._api_params,
            files={"image_file": image},
        )
        self._logger.debug(f"FacePlusPlus response: {result}")
        if "error_message" in result:
            raise ExternalValueError(result["error_message"])
        image_id = "".join(filter(str.isalnum, result["image_id"]))
        return Image(
            id=image_id,
            data=image,
            faces=[
                Face(
                    id=face["face_token"],
                    x=face["face_rectangle"]["left"],
                    y=face["face_rectangle"]["top"],
                    width=face["face_rectangle"]["width"],
                    height=face["face_rectangle"]["height"],
                )
                for face in result["faces"]
            ],
        )

    async def compare(self, face_token_1: str, face_token_2: str) -> float:
        result = await self._http_client.post(
            url=f"{self._api_url}/compare",
            params={
                **self._api_params,
                "face_token1": face_token_1,
                "face_token2": face_token_2,
            },
        )
        self._logger.debug(f"FacePlusPlus response: {result}")
        if "error_message" in result:
            raise ExternalValueError(result["error_message"])
        return result["confidence"]
